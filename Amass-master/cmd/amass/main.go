// Copyright 2017 Jeff Foley. All rights reserved.
// Use of this source code is governed by Apache 2 LICENSE that can be found in the LICENSE file.

package main

import (
	"bytes"
	"flag"
	"fmt"
	"os"
	"path"

	"github.com/OWASP/Amass/config"
	"github.com/OWASP/Amass/eventbus"
	"github.com/OWASP/Amass/resolvers"
	"github.com/OWASP/Amass/services/sources"
	"github.com/OWASP/Amass/utils"
	"github.com/fatih/color"
)

const (
	mainUsageMsg         = "intel|enum|viz|track|db [options]"
	exampleConfigFileURL = "https://github.com/OWASP/Amass/blob/master/examples/config.ini"
	userGuideURL         = "https://github.com/OWASP/Amass/blob/master/doc/user_guide.md"
)

var (
	// Colors used to ease the reading of program output
	y      = color.New(color.FgHiYellow)
	g      = color.New(color.FgHiGreen)
	r      = color.New(color.FgHiRed)
	b      = color.New(color.FgHiBlue)
	fgR    = color.New(color.FgRed)
	fgY    = color.New(color.FgYellow)
	yellow = color.New(color.FgHiYellow).SprintFunc()
	green  = color.New(color.FgHiGreen).SprintFunc()
	blue   = color.New(color.FgHiBlue).SprintFunc()
)

func commandUsage(msg string, cmdFlagSet *flag.FlagSet, errBuf *bytes.Buffer) {
	utils.PrintBanner()
	g.Fprintf(color.Error, "Usage: %s %s\n\n", path.Base(os.Args[0]), msg)
	cmdFlagSet.PrintDefaults()
	g.Fprintln(color.Error, errBuf.String())

	if msg == mainUsageMsg {
		g.Fprintf(color.Error, "\nSubcommands: \n\n")
		g.Fprintf(color.Error, "\t%-11s - Discover targets for enumerations\n", "amass intel")
		g.Fprintf(color.Error, "\t%-11s - Perform enumerations and network mapping\n", "amass enum")
		g.Fprintf(color.Error, "\t%-11s - Visualize enumeration results\n", "amass viz")
		g.Fprintf(color.Error, "\t%-11s - Track differences between enumerations\n", "amass track")
		g.Fprintf(color.Error, "\t%-11s - Manipulate the Amass graph database\n\n", "amass db")
	}

	g.Fprintf(color.Error, "The user's guide can be found here: \n%s\n\n", userGuideURL)
	g.Fprintf(color.Error, "An example configuration file can be found here: \n%s\n\n", exampleConfigFileURL)
}

func main() {
	var version, help1, help2 bool
	mainFlagSet := flag.NewFlagSet("amass", flag.ContinueOnError)

	defaultBuf := new(bytes.Buffer)
	mainFlagSet.SetOutput(defaultBuf)

	mainFlagSet.BoolVar(&help1, "h", false, "Show the program usage message")
	mainFlagSet.BoolVar(&help2, "help", false, "Show the program usage message")
	mainFlagSet.BoolVar(&version, "version", false, "Print the version number of this Amass binary")

	if len(os.Args) < 2 {
		commandUsage(mainUsageMsg, mainFlagSet, defaultBuf)
		return
	}

	if err := mainFlagSet.Parse(os.Args[1:]); err != nil {
		r.Fprintf(color.Error, "%v\n", err)
		os.Exit(1)
	}
	if help1 || help2 {
		commandUsage(mainUsageMsg, mainFlagSet, defaultBuf)
		return
	}
	if version {
		fmt.Fprintf(color.Error, "%s\n", utils.Version)
		return
	}

	switch os.Args[1] {
	case "db":
		runDBCommand(os.Args[2:])
	case "enum":
		runEnumCommand(os.Args[2:])
	case "intel":
		runIntelCommand(os.Args[2:])
	case "track":
		runTrackCommand(os.Args[2:])
	case "viz":
		runVizCommand(os.Args[2:])
	default:
		commandUsage(mainUsageMsg, mainFlagSet, defaultBuf)
		os.Exit(1)
	}
}

// GetAllSourceNames returns the names of all Amass data sources.
func GetAllSourceNames() []string {
	bus := eventbus.NewEventBus()

	var names []string
	for _, src := range sources.GetAllSources(&config.Config{}, bus, resolvers.NewResolverPool(nil)) {
		names = append(names, src.String())
	}
	bus.Stop()
	return names
}
