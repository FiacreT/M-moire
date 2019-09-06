// Copyright 2017 Jeff Foley. All rights reserved.
// Use of this source code is governed by Apache 2 LICENSE that can be found in the LICENSE file.

package sources

import (
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"github.com/OWASP/Amass/config"
	eb "github.com/OWASP/Amass/eventbus"
	"github.com/OWASP/Amass/requests"
	"github.com/OWASP/Amass/resolvers"
	"github.com/OWASP/Amass/services"
	"github.com/OWASP/Amass/utils"
	"github.com/dghubble/go-twitter/twitter"
	"golang.org/x/oauth2"
)

// Twitter is the Service that handles access to the Twitter data source.
type Twitter struct {
	services.BaseService

	API        *config.APIKey
	SourceType string
	RateLimit  time.Duration
	client     *twitter.Client
}

// NewTwitter returns he object initialized, but not yet started.
func NewTwitter(cfg *config.Config, bus *eb.EventBus, pool *resolvers.ResolverPool) *Twitter {
	t := &Twitter{
		SourceType: requests.API,
		RateLimit:  3 * time.Second,
	}

	t.BaseService = *services.NewBaseService(t, "Twitter", cfg, bus, pool)
	return t
}

// OnStart implements the Service interface
func (t *Twitter) OnStart() error {
	t.BaseService.OnStart()

	t.API = t.Config().GetAPIKey(t.String())
	if t.API == nil || t.API.Key == "" || t.API.Secret == "" {
		t.Bus().Publish(requests.LogTopic,
			fmt.Sprintf("%s: API key data was not provided", t.String()),
		)
	}
	if t.API != nil && t.API.Key != "" && t.API.Secret != "" {
		if bearer, err := t.getBearerToken(); err == nil {
			config := &oauth2.Config{}
			token := &oauth2.Token{AccessToken: bearer}
			// OAuth2 http.Client will automatically authorize Requests
			httpClient := config.Client(oauth2.NoContext, token)
			// Twitter client
			t.client = twitter.NewClient(httpClient)
		}
	}

	go t.processRequests()
	return nil
}

func (t *Twitter) processRequests() {
	last := time.Now()

	for {
		select {
		case <-t.Quit():
			return
		case req := <-t.DNSRequestChan():
			if t.Config().IsDomainInScope(req.Domain) {
				if time.Now().Sub(last) < t.RateLimit {
					time.Sleep(t.RateLimit)
				}
				last = time.Now()
				t.executeQuery(req.Domain)
				last = time.Now()
			}
		case <-t.AddrRequestChan():
		case <-t.ASNRequestChan():
		case <-t.WhoisRequestChan():
		}
	}
}

func (t *Twitter) executeQuery(domain string) {
	re := t.Config().DomainRegex(domain)
	if t.client == nil || re == nil {
		return
	}

	searchParams := &twitter.SearchTweetParams{
		Query: domain,
		Count: 100,
	}
	t.SetActive()
	search, _, err := t.client.Search.Tweets(searchParams)
	if err != nil {
		t.Bus().Publish(requests.LogTopic, fmt.Sprintf("%s: %v", t.String(), err))
		return
	}

	for _, tweet := range search.Statuses {

		// Urls in the tweet body
		for _, urlEntity := range tweet.Entities.Urls {
			for _, name := range re.FindAllString(urlEntity.ExpandedURL, -1) {
				t.Bus().Publish(requests.NewNameTopic, &requests.DNSRequest{
					Name:   name,
					Domain: domain,
					Tag:    t.SourceType,
					Source: t.String(),
				})
			}
		}

		// Source of the tweet
		for _, name := range re.FindAllString(tweet.Source, -1) {
			t.Bus().Publish(requests.NewNameTopic, &requests.DNSRequest{
				Name:   name,
				Domain: domain,
				Tag:    t.SourceType,
				Source: t.String(),
			})
		}
	}
}

func (t *Twitter) getBearerToken() (string, error) {
	headers := map[string]string{"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
	page, err := utils.RequestWebPage(
		"https://api.twitter.com/oauth2/token",
		strings.NewReader("grant_type=client_credentials"),
		headers, t.API.Key, t.API.Secret)
	if err != nil {
		return "", fmt.Errorf("token request failed: %+v", err)
	}

	var v struct {
		AccessToken string `json:"access_token"`
	}
	if err := json.Unmarshal([]byte(page), &v); err != nil {
		return "", fmt.Errorf("error parsing json in token response: %+v", err)
	}
	if v.AccessToken == "" {
		return "", fmt.Errorf("token response does not have access_token")
	}
	return v.AccessToken, nil
}
