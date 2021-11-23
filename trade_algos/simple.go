package trade_algos

import (
	"encoding/csv"
	"fmt"
	"os"
	"os/signal"
	"strconv"
	"sync"
	"syscall"
	"time"

	"github.com/CasualCodersProjects/autostonks/trader"
)

type SimpleAlgoInput struct {
	Ticker string
	Qty float64
	MinGain float64
	MaxLoss float64
}

func ReadCSVFile(file string) ([]SimpleAlgoInput, error) {
	// read the CSV file
	f, err := os.Open(file)

	if err != nil {
		return nil, err
	}

	defer f.Close()

	// create a new CSV reader
	reader := csv.NewReader(f)
	
	// read all lines
	lines, err := reader.ReadAll()

	if err != nil {
		return nil, err
	}

	// create a new array of SimpleAlgoInput
	inputs := make([]SimpleAlgoInput, len(lines))

	// loop through all lines
	for i, line := range lines {

		qty, err := strconv.ParseFloat(line[1], 64)
		
		if err != nil {
			return nil, err
		}

		minGain, err := strconv.ParseFloat(line[2], 64)

		if err != nil {
			return nil, err
		}

		maxLoss, err := strconv.ParseFloat(line[3], 64)

		if err != nil {
			return nil, err
		}

		inputs[i] = SimpleAlgoInput{
			Ticker: line[0],
			Qty: qty,
			MinGain: minGain,
			MaxLoss: maxLoss,
		}
	}

	return inputs, nil
}

func SimpleAlgoWorker(trades *trader.Trader, ticker string, qty float64, min_gain, max_loss float64, wg *sync.WaitGroup, quit chan os.Signal) {
	defer wg.Done()
	fmt.Println("Starting trading thread for " + ticker)
	for {
		select {
		case <-quit:
			fmt.Println("Quitting trading thread for " + ticker)
			return
		default:
			// check if the market is open
			marketOpen, err := trades.IsMarketOpen()

			if err != nil {
				fmt.Println(err)
				break
			}

			if !marketOpen {
				// sleep for a minute
				time.Sleep(time.Minute)
				continue
			}
			
			// check if we own any shares of the given ticker
			shares, err := trades.GetNumberOfShares(ticker)

			if err != nil {
				fmt.Println(err)
				break
			}
			
			if shares == 0 {
				fmt.Println("No shares of " + ticker + " owned. Buying shares...")
				// buy a share
				err = trades.Buy(ticker, qty)

				if err != nil {
					fmt.Println(err)
					break
				}
			}

			// get the current price of the given ticker
			price, err := trades.GetPrice(ticker)

			if err != nil {
				fmt.Println(err)
				break
			}

			// get the purchase price of the given ticker
			buyPrice, err := trades.GetBuyPrice(ticker)

			if err != nil {
				fmt.Println(err)
				break
			}

			// get the gain/loss of the given ticker
			gainLoss := price - buyPrice

			fmt.Println("Gain/Loss of " + ticker + ": " + fmt.Sprintf("%.2f", gainLoss))

			if gainLoss >= min_gain {
				// sell the given ticker
				err = trades.Sell(ticker, qty)
			} else if gainLoss <= max_loss {
				// sell the given ticker
				err = trades.Sell(ticker, qty)
			}

			if err != nil {
				fmt.Println(err)
				break
			}

			// sleep for a 10 seconds
			time.Sleep(time.Second * 10)
		}

		fmt.Println("Stopping trading thread for " + ticker)
	}
}

func SimpleAlgorithm(inputFileName string) {
	// read the CSV file
	inputs, err := ReadCSVFile(inputFileName)

	if err != nil {
		panic(err)
	}

	// create a new trader
	trades := trader.NewTrader(os.Getenv("API_KEY"), os.Getenv("API_SECRET"), os.Getenv("BASE_URL"))

	// create a new workgroup
	var wg = &sync.WaitGroup{}

	// create a new channel to receive os.Signals
	quit := make(chan os.Signal, len(inputs)) // buffered
	signal.Notify(quit, syscall.SIGHUP, syscall.SIGINT, syscall.SIGTERM, syscall.SIGQUIT)


	// loop through all inputs
	for _, input := range inputs {
		// add the worker to the workgroup
		wg.Add(1)

		// start a new worker
		go SimpleAlgoWorker(trades, input.Ticker, input.Qty, input.MinGain, input.MaxLoss, wg, quit)
	}

	// wait for all workers to finish
	wg.Wait()
}