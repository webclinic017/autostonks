package trader

import (
	"github.com/alpacahq/alpaca-trade-api-go/v2/alpaca"
	"github.com/alpacahq/alpaca-trade-api-go/v2/marketdata"
	"github.com/shopspring/decimal"
	"github.com/uniplaces/carbon"
)

type Trader struct {
	MarketData marketdata.Client 
	ApiClient alpaca.Client
}

func NewTrader(apiKey string, apiSecret string) *Trader {

	marketDataParams := marketdata.ClientOpts{
		ApiKey:  apiKey,
		ApiSecret: apiSecret,
	}

	apiClientParams := alpaca.ClientOpts{
		ApiKey:  apiKey,
		ApiSecret: apiSecret,
	}

	return &Trader{
		MarketData: marketdata.NewClient(marketDataParams),
		ApiClient: alpaca.NewClient(apiClientParams),
	}
}


// get number of shares the user owns for a given
// ticker symbol
func (trader *Trader) GetNumberOfShares(ticker string) (float64, error) {
	// get the number of shares a user owns
	position, err := trader.ApiClient.GetPosition(ticker)

	if err != nil {
		return 0, err
	}

	return position.Qty.InexactFloat64(), nil
}

func (trader *Trader) GetCurrentValueOfShares(ticker string) (float64, error) {
	shares, err := trader.GetNumberOfShares(ticker)

	if err != nil {
		return 0, err
	}

	price, err := trader.GetPrice(ticker)

	if err != nil {
		return 0, err
	}

	return shares * price, nil
}

func (trader *Trader) HasTradedToday() (bool, error) {
	status := "closed"
	limit := 500
	nested := false

	orders, err := trader.ApiClient.ListOrders(&status, nil, &limit, &nested)

	if err != nil {
		return false, err
	}

	for _, order := range orders {
		if order.Side == "buy" {
			fillTimeUnix := order.FilledAt.UTC().Unix()
			fillTime, err := carbon.CreateFromTimestampUTC(fillTimeUnix)
			if err != nil {
				return false, err
			}
			if fillTime.IsToday() {
				return true, nil
			}
		}
	}

	return false, nil
}

func (trader *Trader) GetAccountValue(ticker string) (float64, error) {
	account, err := trader.ApiClient.GetAccount()

	if err != nil {
		return 0, err
	}

	return account.PortfolioValue.InexactFloat64(), nil
}

func (trader *Trader) GetAccountCash() (float64, error) {
	account, err := trader.ApiClient.GetAccount()

	if err != nil {
		return 0, err
	}

	return account.Cash.InexactFloat64(), nil
}

func (trader *Trader) GetAccountEquity() (float64, error) {
	account, err := trader.ApiClient.GetAccount()

	if err != nil {
		return 0, err
	}

	return account.Equity.InexactFloat64(), nil
}

func (trader *Trader) GetAccountBuyingPower() (float64, error) {
	account, err := trader.ApiClient.GetAccount()

	if err != nil {
		return 0, err
	}

	return account.BuyingPower.InexactFloat64(), nil
}

func (trader *Trader) ClearOrders() error {
	status := "open"
	limit := 500
	nested := false

	orders, err := trader.ApiClient.ListOrders(&status, nil, &limit, &nested)

	if err != nil {
		return err
	}

	for _, order := range orders {
		if err := trader.ApiClient.CancelOrder(order.ID); err != nil {
			return err
		}
	}

	return nil
}

func (trader *Trader) BuyNotional(ticker string, notional float64) error {

	notionalDecimal := decimal.NewFromFloat(notional)

	orderReq := alpaca.PlaceOrderRequest{
		AssetKey: &ticker,
		Notional: &notionalDecimal,
		Side:     "buy",
		Type:     "market",
		TimeInForce: "day",
	}

	_, err := trader.ApiClient.PlaceOrder(orderReq)

	return err
}

func (trader *Trader) SellNotional(ticker string, notional float64) error {

	notionalDecimal := decimal.NewFromFloat(notional)

	orderReq := alpaca.PlaceOrderRequest{
		AssetKey: &ticker,
		Notional: &notionalDecimal,
		Side:     "sell",
		Type:     "market",
		TimeInForce: "day",
	}

	_, err := trader.ApiClient.PlaceOrder(orderReq)

	return err
}

func (trader *Trader) Buy(ticker string, qty float64) error {
	
	qtyDecimal := decimal.NewFromFloat(qty)

	orderReq := alpaca.PlaceOrderRequest{
		AssetKey: &ticker,
		Qty:      &qtyDecimal,
		Side:     "buy",
		Type:     "limit",
		TimeInForce: "day",
	}

	_, err := trader.ApiClient.PlaceOrder(orderReq)

	return err
}

func (trader *Trader) Sell(ticker string, qty float64) error {
	
	qtyDecimal := decimal.NewFromFloat(qty)

	orderReq := alpaca.PlaceOrderRequest{
		AssetKey: &ticker,
		Qty:      &qtyDecimal,
		Side:     "sell",
		Type:     "limit",
		TimeInForce: "day",
	}

	_, err := trader.ApiClient.PlaceOrder(orderReq)

	return err
}

// get current price for a given ticker symbol
func (trader *Trader) GetPrice(ticker string) (float64, error) {
	
	bar, err := trader.MarketData.GetLatestBar(ticker)

	if err != nil {
		return 0, err
	}

	return bar.Close, nil
}

// get current price for a given crypto
func (trader *Trader) GetCryptoPrice(crypto string) (float64, error) {

	params := marketdata.GetCryptoBarsParams{
		TotalLimit: 1,
	}
	
	bars, err := trader.MarketData.GetCryptoBars(crypto, params)

	if err != nil {
		return 0, err
	}

	bar := bars[0]

	return bar.Close, nil
}

// is the market open
func (trader *Trader) IsMarketOpen() (bool, error) {
	
	// get clock
	clock, err := trader.ApiClient.GetClock()

	if err != nil {
		return false, err
	}

	return clock.IsOpen, nil
}

