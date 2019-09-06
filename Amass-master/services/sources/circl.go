// Copyright 2017 Jeff Foley. All rights reserved.
// Use of this source code is governed by Apache 2 LICENSE that can be found in the LICENSE file.

package sources

import (
	"bufio"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/OWASP/Amass/config"
	eb "github.com/OWASP/Amass/eventbus"
	"github.com/OWASP/Amass/requests"
	"github.com/OWASP/Amass/resolvers"
	"github.com/OWASP/Amass/services"
	"github.com/OWASP/Amass/stringset"
	"github.com/OWASP/Amass/utils"
)

// CIRCL is the Service that handles access to the CIRCL data source.
type CIRCL struct {
	services.BaseService

	API        *config.APIKey
	SourceType string
	RateLimit  time.Duration
}

// NewCIRCL returns he object initialized, but not yet started.
func NewCIRCL(cfg *config.Config, bus *eb.EventBus, pool *resolvers.ResolverPool) *CIRCL {
	c := &CIRCL{
		SourceType: requests.API,
		RateLimit:  time.Second,
	}

	c.BaseService = *services.NewBaseService(c, "CIRCL", cfg, bus, pool)
	return c
}

// OnStart implements the Service interface
func (c *CIRCL) OnStart() error {
	c.BaseService.OnStart()

	c.API = c.Config().GetAPIKey(c.String())
	if c.API == nil || c.API.Username == "" || c.API.Password == "" {
		c.Bus().Publish(requests.LogTopic, fmt.Sprintf("%s: API key data was not provided", c.String()))
	}

	go c.processRequests()
	return nil
}

func (c *CIRCL) processRequests() {
	last := time.Now()

	for {
		select {
		case <-c.Quit():
			return
		case req := <-c.DNSRequestChan():
			if c.Config().IsDomainInScope(req.Domain) {
				if time.Now().Sub(last) < c.RateLimit {
					time.Sleep(c.RateLimit)
				}
				last = time.Now()
				c.executeQuery(req.Domain)
				last = time.Now()
			}
		case <-c.AddrRequestChan():
		case <-c.ASNRequestChan():
		case <-c.WhoisRequestChan():
		}
	}
}

func (c *CIRCL) executeQuery(domain string) {
	if c.API == nil || c.API.Username == "" || c.API.Password == "" {
		return
	}

	c.SetActive()
	url := c.restURL(domain)
	headers := map[string]string{"Content-Type": "application/json"}
	page, err := utils.RequestWebPage(url, nil, headers, c.API.Username, c.API.Password)
	if err != nil {
		c.Bus().Publish(requests.LogTopic, fmt.Sprintf("%s: %s: %v", c.String(), url, err))
		return
	}

	c.passiveDNSJSON(page, domain)
}

func (c *CIRCL) restURL(domain string) string {
	return "https://www.circl.lu/pdns/query/" + domain
}

func (c *CIRCL) passiveDNSJSON(page, domain string) {
	unique := stringset.New()

	re := c.Config().DomainRegex(domain)
	if re == nil {
		return
	}

	c.SetActive()
	scanner := bufio.NewScanner(strings.NewReader(page))
	for scanner.Scan() {
		// Get the next line of JSON
		line := scanner.Text()
		if line == "" {
			continue
		}

		var j struct {
			Name string `json:"rrname"`
		}
		err := json.Unmarshal([]byte(line), &j)
		if err != nil {
			continue
		}
		if re.MatchString(j.Name) {
			unique.Insert(j.Name)
		}
	}

	for name := range unique {
		c.Bus().Publish(requests.NewNameTopic, &requests.DNSRequest{
			Name:   name,
			Domain: domain,
			Tag:    c.SourceType,
			Source: c.String(),
		})
	}
}
