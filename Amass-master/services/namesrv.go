// Copyright 2017 Jeff Foley. All rights reserved.
// Use of this source code is governed by Apache 2 LICENSE that can be found in the LICENSE file.

package services

import (
	"regexp"
	"strings"
	"time"

	"github.com/OWASP/Amass/config"
	eb "github.com/OWASP/Amass/eventbus"
	"github.com/OWASP/Amass/graph"
	"github.com/OWASP/Amass/requests"
	"github.com/OWASP/Amass/resolvers"
	"github.com/OWASP/Amass/utils"
)

var (
	topNames = []string{
		"www",
		"online",
		"webserver",
		"ns1",
		"mail",
		"smtp",
		"webmail",
		"prod",
		"test",
		"vpn",
		"ftp",
		"ssh",
	}
)

type timesRequest struct {
	Subdomain string
	Times     chan int
}

// NameService is the Service that handles all newly discovered names
// within the architecture. This is achieved by receiving all the RESOLVED events.
type NameService struct {
	BaseService

	filter            *utils.StringFilter
	times             *utils.Queue
	sanityRE          *regexp.Regexp
	trustedNameFilter *utils.StringFilter
	otherNameFilter   *utils.StringFilter
	graph             graph.DataHandler
}

// NewNameService requires the enumeration configuration and event bus as parameters.
// The object returned is initialized, but has not yet been started.
func NewNameService(cfg *config.Config, bus *eb.EventBus, pool *resolvers.ResolverPool) *NameService {
	ns := &NameService{
		filter:            utils.NewStringFilter(),
		times:             new(utils.Queue),
		sanityRE:          utils.AnySubdomainRegex(),
		trustedNameFilter: utils.NewStringFilter(),
		otherNameFilter:   utils.NewStringFilter(),
	}
	ns.BaseService = *NewBaseService(ns, "Name Service", cfg, bus, pool)
	return ns
}

// OnStart implements the Service interface
func (ns *NameService) OnStart() error {
	ns.BaseService.OnStart()

	ns.Bus().Subscribe(requests.NewNameTopic, ns.newNameEvent)
	ns.Bus().Subscribe(requests.NameResolvedTopic, ns.Resolved)
	go ns.processTimesRequests()
	go ns.processRequests()
	return nil
}

// RegisterGraph makes the Graph available to the NameService.
func (ns *NameService) RegisterGraph(g graph.DataHandler) {
	ns.graph = g
}

func (ns *NameService) newNameEvent(req *requests.DNSRequest) {
	if req == nil || req.Name == "" || req.Domain == "" {
		return
	}

	req.Name = strings.ToLower(utils.RemoveAsteriskLabel(req.Name))
	req.Domain = strings.ToLower(req.Domain)

	tt := requests.TrustedTag(req.Tag)
	if !tt && ns.otherNameFilter.Duplicate(req.Name) {
		return
	} else if tt && ns.trustedNameFilter.Duplicate(req.Name) {
		return
	}
	ns.SendDNSRequest(req)
}

func (ns *NameService) processRequests() {
	for {
		select {
		case <-ns.PauseChan():
			<-ns.ResumeChan()
		case <-ns.Quit():
			return
		case req := <-ns.DNSRequestChan():
			ns.performRequest(req)
		case <-ns.AddrRequestChan():
		case <-ns.ASNRequestChan():
		case <-ns.WhoisRequestChan():
		}
	}
}

func (ns *NameService) performRequest(req *requests.DNSRequest) {
	ns.SetActive()
	if ns.Config().Passive {
		if !ns.filter.Duplicate(req.Name) && ns.sanityRE.MatchString(req.Name) {
			ns.Bus().Publish(requests.OutputTopic, &requests.Output{
				Name:   req.Name,
				Domain: req.Domain,
				Tag:    req.Tag,
				Source: req.Source,
			})
		}
		return
	}
	ns.Bus().Publish(requests.ResolveNameTopic, req)
}

// Resolved is called when a name has been resolved by the DNS Service.
func (ns *NameService) Resolved(req *requests.DNSRequest) {
	ns.SetActive()

	if ns.Config().IsDomainInScope(req.Name) {
		ns.checkSubdomain(req)

		if ns.Config().BruteForcing && ns.Config().Recursive {
			for _, name := range topNames {
				go ns.newNameEvent(&requests.DNSRequest{
					Name:   name + "." + req.Name,
					Domain: req.Domain,
					Tag:    requests.ALT,
					Source: ns.String(),
				})
			}
		}
	}
}

func (ns *NameService) checkSubdomain(req *requests.DNSRequest) {
	labels := strings.Split(req.Name, ".")
	num := len(labels)
	// Is this large enough to consider further?
	if num < 2 {
		return
	}
	// It cannot have fewer labels than the root domain name
	if num-1 < len(strings.Split(req.Domain, ".")) {
		return
	}
	// Do not further evaluate service subdomains
	if labels[1] == "_tcp" || labels[1] == "_udp" || labels[1] == "_tls" {
		return
	}

	sub := strings.Join(labels[1:], ".")
	if ns.graph != nil {
		// CNAMEs are not a proper subdomain
		cname := ns.graph.IsCNAMENode(&graph.DataOptsParams{
			UUID:   ns.Config().UUID.String(),
			Name:   sub,
			Domain: req.Domain,
		})
		if cname {
			return
		}
	}

	ns.Bus().Publish(requests.NewSubdomainTopic, &requests.DNSRequest{
		Name:   sub,
		Domain: req.Domain,
		Tag:    req.Tag,
		Source: req.Source,
	}, ns.timesForSubdomain(sub))
}

func (ns *NameService) timesForSubdomain(sub string) int {
	times := make(chan int)

	ns.times.Append(&timesRequest{
		Subdomain: sub,
		Times:     times,
	})
	return <-times
}

func (ns *NameService) processTimesRequests() {
	curIdx := 0
	maxIdx := 9
	delays := []int{10, 25, 50, 75, 100, 150, 250, 500, 750, 1000}
	subdomains := make(map[string]int)

	for {
		select {
		case <-ns.Quit():
			return
		default:
			element, ok := ns.times.Next()
			if !ok {
				if curIdx < maxIdx {
					curIdx++
				}
				time.Sleep(time.Duration(delays[curIdx]) * time.Millisecond)
				continue
			}

			curIdx = 0
			req := element.(*timesRequest)
			times, ok := subdomains[req.Subdomain]
			if ok {
				times++
			} else {
				times = 1
			}
			subdomains[req.Subdomain] = times
			req.Times <- times
		}
	}
}
