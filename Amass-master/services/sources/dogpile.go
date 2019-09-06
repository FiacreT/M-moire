// Copyright 2017 Jeff Foley. All rights reserved.
// Use of this source code is governed by Apache 2 LICENSE that can be found in the LICENSE file.

package sources

import (
	"fmt"
	"net/url"
	"strconv"
	"time"

	"github.com/OWASP/Amass/config"
	eb "github.com/OWASP/Amass/eventbus"
	"github.com/OWASP/Amass/requests"
	"github.com/OWASP/Amass/resolvers"
	"github.com/OWASP/Amass/services"
	"github.com/OWASP/Amass/utils"
)

// Dogpile is the Service that handles access to the Dogpile data source.
type Dogpile struct {
	services.BaseService

	quantity   int
	limit      int
	SourceType string
}

// NewDogpile returns he object initialized, but not yet started.
func NewDogpile(cfg *config.Config, bus *eb.EventBus, pool *resolvers.ResolverPool) *Dogpile {
	d := &Dogpile{
		quantity:   15, // Dogpile returns roughly 15 results per page
		limit:      90,
		SourceType: requests.SCRAPE,
	}

	d.BaseService = *services.NewBaseService(d, "Dogpile", cfg, bus, pool)
	return d
}

// OnStart implements the Service interface
func (d *Dogpile) OnStart() error {
	d.BaseService.OnStart()

	go d.processRequests()
	return nil
}

func (d *Dogpile) processRequests() {
	for {
		select {
		case <-d.Quit():
			return
		case req := <-d.DNSRequestChan():
			if d.Config().IsDomainInScope(req.Domain) {
				d.executeQuery(req.Domain)
			}
		case <-d.AddrRequestChan():
		case <-d.ASNRequestChan():
		case <-d.WhoisRequestChan():
		}
	}
}

func (d *Dogpile) executeQuery(domain string) {
	re := d.Config().DomainRegex(domain)
	if re == nil {
		return
	}

	num := d.limit / d.quantity
	t := time.NewTicker(time.Second)
	defer t.Stop()

	for i := 0; i < num; i++ {
		d.SetActive()

		select {
		case <-d.Quit():
			return
		case <-t.C:
			u := d.urlByPageNum(domain, i)
			page, err := utils.RequestWebPage(u, nil, nil, "", "")
			if err != nil {
				d.Bus().Publish(requests.LogTopic, fmt.Sprintf("%s: %s: %v", d.String(), u, err))
				return
			}

			for _, sd := range re.FindAllString(page, -1) {
				d.Bus().Publish(requests.NewNameTopic, &requests.DNSRequest{
					Name:   cleanName(sd),
					Domain: domain,
					Tag:    d.SourceType,
					Source: d.String(),
				})
			}
		}
	}
}

func (d *Dogpile) urlByPageNum(domain string, page int) string {
	qsi := strconv.Itoa(d.quantity * page)
	u, _ := url.Parse("http://www.dogpile.com/search/web")

	u.RawQuery = url.Values{"qsi": {qsi}, "q": {domain}}.Encode()
	return u.String()
}
