package main

import (
	"fmt"
	"os"

	"github.com/akamensky/argparse"
	"github.com/joho/godotenv"
)

func main() {

	err := godotenv.Load()

	if err != nil {
		fmt.Println("Dotenv not found, checking environment...")
		// check environment for API_KEY and API_SECRET
		if os.Getenv("API_KEY") == "" || os.Getenv("API_SECRET") == "" {
			fmt.Println("API_KEY and API_SECRET not found in environment!")
			os.Exit(1)
		} else {
			fmt.Println("API_KEY and API_SECRET found in environment.")
		}
	}

	// Create new parser object
	parser := argparse.NewParser("autostonks", "Buys and sells stocks on the Alpaca Market based on a set of algorithms.")
	// Create string flag
	t := parser.Flag("t", "test", &argparse.Options{Required: false, Help: "Prints arguments and exits."})
	a := parser.String("a", "algorithm", &argparse.Options{Required: true, Help: "Algorithm to use."})
	s := parser.String("s", "symbol", &argparse.Options{Required: false, Help: "Symbol to buy or sell."})
	// Parse input
	err = parser.Parse(os.Args)
	if err != nil {
		// In case of error print error and print usage
		// This can also be done by passing -h or --help flags
		fmt.Print(parser.Usage(err))
	}
	
	algorithm := *a
	symbol := *s

	if *t {
		fmt.Println("Algorithm:", algorithm)
		fmt.Println("Symbol:", symbol)
		os.Exit(0)
	}
}