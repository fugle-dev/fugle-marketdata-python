from fugle_marketdata import RestClient
from fugle_marketdata.rest.stock import RestStockClient

import pytest
import requests
from unittest.mock import MagicMock

@pytest.fixture
def api_key_client():
    return RestClient(api_key='api-key')

@pytest.fixture
def bearer_client():
    return RestClient(bearer_token='bearer-token')

class TestRestClientConstructor(object):
    def test_with_apiKey(self):
        # 建立 RestClient 實例並測試是否為 RestClient 物件
        client = RestClient(api_key='api-key')
        assert isinstance(client, RestClient)

    def test_with_bearerToken(self):
        # 建立 RestClient 實例並測試是否為 RestClient 物件
        client = RestClient(bearer_token='bearer-token')
        assert isinstance(client, RestClient)

    def test_with_no_options(self):
        # 測試是否會拋出錯誤
        with pytest.raises(Exception):
            RestClient()

    def test_with_both_apiKey_and_bearerToken(self):
        # 測試是否會拋出錯誤
        with pytest.raises(Exception):
            RestClient(api_key='api-key', bearer_token='bearer-token')



class TestStockRestClient:
    def test_stock_instance(self, api_key_client):
        stock = api_key_client.stock
        assert isinstance(stock, RestStockClient)

    def test_stock_same_instance(self, api_key_client):
        stock1 = api_key_client.stock
        stock2 = api_key_client.stock
        assert stock1 is stock2

class TestStockRestIntradayClient:
    def test_stock_intraday(self, api_key_client):
        stock = api_key_client.stock
        assert hasattr(stock.intraday, 'tickers')
        assert hasattr(stock.intraday, 'ticker')
        assert hasattr(stock.intraday, 'quote')
        assert hasattr(stock.intraday, 'candles')
        assert hasattr(stock.intraday, 'trades')
        assert hasattr(stock.intraday, 'volumes')

    def test_intraday_tickers_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.tickers(type='INDEX')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/tickers?type=INDEX',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_tickers_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.tickers(type='INDEX')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/tickers?type=INDEX',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_intraday_ticker_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.ticker(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/ticker/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_ticker_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.ticker(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/ticker/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )


    def test_intraday_quote_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.quote(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/quote/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_quote_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.quote(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/quote/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_intraday_trades_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.trades(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/trades/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_trades_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.trades(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/trades/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_intraday_volumes_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.volumes(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/volumes/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_volumes_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.volumes(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/intraday/volumes/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

class TestStockRestHistoricalClient:
    def test_stock_historical(self, api_key_client):
        stock = api_key_client.stock
        assert hasattr(stock.historical, 'candles')
        assert hasattr(stock.historical, 'stats')

    def test_historical_candles_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.historical.candles(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/historical/candles/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_historical_candles_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.historical.candles(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/historical/candles/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_historical_stats_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.historical.stats(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/historical/stats/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_historical_stats_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.historical.stats(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/historical/stats/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

class TestStockRestSnapshotClient:
    def test_stock_historical(self, api_key_client):
        stock = api_key_client.stock
        assert hasattr(stock.snapshot, 'quotes')
        assert hasattr(stock.snapshot, 'movers')
        assert hasattr(stock.snapshot, 'actives')

    def test_snapshot_quotes_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.snapshot.quotes(market='TSE')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/snapshot/quotes/TSE',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_snapshot_quotes_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.snapshot.quotes(market='TSE')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/snapshot/quotes/TSE',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_snapshot_movers_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.snapshot.movers(market='TSE', change='percent', direction='up')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/snapshot/movers/TSE?change=percent&direction=up',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_snapshot_movers_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.snapshot.movers(market='TSE', change='percent', direction='up')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/snapshot/movers/TSE?change=percent&direction=up',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_snapshot_actives_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.snapshot.actives(market='TSE', trade='volume')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/snapshot/actives/TSE?trade=volume',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_snapshot_actives_bearer_token(self, bearer_client, mocker):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.snapshot.actives(market='TSE', trade='volume')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/snapshot/actives/TSE?trade=volume',
            headers={'Authorization': 'Bearer bearer-token'}
        )

class TestFutOptRestIntradayClient:
    def test_futopt_intraday(self, api_key_client):
        futopt = api_key_client.futopt
        assert hasattr(futopt.intraday, 'products')
        assert hasattr(futopt.intraday, 'tickers')
        assert hasattr(futopt.intraday, 'ticker')
        assert hasattr(futopt.intraday, 'quote')
        assert hasattr(futopt.intraday, 'candles')
        assert hasattr(futopt.intraday, 'trades')
        assert hasattr(futopt.intraday, 'volumes')

    def test_intraday_products_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.intraday.products(type='OPTION')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/intraday/products?type=OPTION',
            headers={'X-API-KEY': 'api-key'}
        )
    
    def test_intraday_tickers_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.intraday.tickers(type='OPTION')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/intraday/tickers?type=OPTION',
            headers={'X-API-KEY': 'api-key'}
        )
    
    def test_intraday_ticker_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.intraday.ticker(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/intraday/ticker/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_quote_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.intraday.quote(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/intraday/quote/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_candles_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.intraday.candles(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/intraday/candles/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_trades_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.intraday.trades(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/intraday/trades/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_intraday_volumes_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.intraday.volumes(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/intraday/volumes/2330',
            headers={'X-API-KEY': 'api-key'}
        )
