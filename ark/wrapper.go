package ark

import (
	"github.com/imroc/req"
)

// Base URL for the ARK data API.
const ARK_BASE_URL string = "https://arkfunds.io/api"
// API Version
const ARK_VERSION string = "v2"
// Combined URL that is executed
const ARK_URL string = ARK_BASE_URL + "/" + ARK_VERSION

// ETFHolding represents a single holding of an ETF.
type ETFHolding struct {
	Ticker string `json:"ticker"`
	Shares float64  `json:"shares"`
	Fund string `json:"fund"`
	MarketValue float64 `json:"market_value"`
	SharePrice float64 `json:"share_price"`
	Company string `json:"company"`
	Date string `json:"date"`
	Cusip string `json:"cusip"`
	Weight float64 `json:"weight"`
	WeightRank int `json:"weight_rank"`
}

// Represents list of holdings for an ETF.
type ETFHoldingResponse struct {
	Holdings []ETFHolding `json:"holdings"`
	DateTo string `json:"date_to"`
	DateFrom string `json:"date_from"`
	Symbol string `json:"symbol"`
}

// Gets the ETF holdings for a given ticker.
func GetETFHoldings(symbol string) (ETFHoldingResponse, error) {
	url := ARK_URL + "/etf/holdings"
	
	params := req.QueryParam{
		"symbol": symbol,
		"limit": 500,
	}

	resp, err := req.Get(url, params)

	if err != nil {
		return ETFHoldingResponse{}, err
	}

	var holdings ETFHoldingResponse

	err = resp.ToJSON(&holdings)

	if err != nil {
		return ETFHoldingResponse{}, err
	}

	return holdings, nil
}

// ETFTrade represents a single trade for an ETF.
type ETFTrade struct {
	Ticker string `json:"ticker"`
	Company string `json:"company"`
	Date string `json:"date"`
	Shares float64 `json:"shares"`
	ETFPercent float64 `json:"etf_percent"`
	Direction string `json:"direction"`
	Fund string `json:"fund"`
	Cusip string `json:"cusip"`
}

// ETFTradesResponse represents a response from the ARK API for a list of trades for an ETF.
type ETFTradesResponse struct {
	Trades []ETFTrade `json:"trades"`
	DateTo string `json:"date_to"`
	DateFrom string `json:"date_from"`
	Symbol string `json:"symbol"`
}

// Gets the ETF trades for a given ticker.
func GetETFTrades(symbol string) (ETFTradesResponse, error) {
	url := ARK_URL + "/etf/trades"

	params := req.QueryParam{
		"symbol": symbol,
	}

	resp, err := req.Get(url, params)

	if err != nil {
		return ETFTradesResponse{}, err
	}

	var trades ETFTradesResponse

	err = resp.ToJSON(&trades)

	if err != nil {
		return ETFTradesResponse{}, err
	}

	return trades, nil
}

