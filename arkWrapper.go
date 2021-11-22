package main

import (
	"github.com/imroc/req"
	"github.com/uniplaces/carbon"
)

const ARK_BASE_URL string = "https://arkfunds.io/api"
const ARK_VERSION string = "v2"
const ARK_URL string = ARK_BASE_URL + "/" + ARK_VERSION

func GetETFHoldings(symbol string) (map[string]string, error) {
	// this needs fixed to return an interface so that 
	// nested JSON can be parsed

	url := ARK_URL + "/etf/holdings"
	
	// get date as YYYY-MM-DD using carbon
	today := carbon.Now().DateString()
	yesterday := carbon.Now().AddDays(-1).DateString()

	params := req.QueryParam{
		"symbol": symbol,
		"start_date": yesterday,
		"end_date": today,
		"limit": 500,
	}

	resp, err := req.Get(url, params)

	if err != nil {
		return nil, err
	}

	ret_map := make(map[string]string)

	resp.ToJSON(&ret_map)

	return ret_map, nil
}

func GetETFTrades(symbol string) (map[string]string, error) {
	return nil, nil
}

