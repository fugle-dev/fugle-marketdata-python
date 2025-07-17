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

@pytest.fixture
def custom_base_url_client():
    return RestClient(api_key='test-key', base_url='https://custom-api.example.com/v2.0')

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

    def test_with_custom_base_url(self):
        # 測試自訂 base_url 是否正確設定
        client = RestClient(api_key='api-key', base_url='https://custom-api.example.com/v2.0')
        assert isinstance(client, RestClient)
        assert client.options['base_url'] == 'https://custom-api.example.com/v2.0'



class TestStockRestClient:
    def test_stock_instance(self, api_key_client):
        stock = api_key_client.stock
        assert isinstance(stock, RestStockClient)

    def test_stock_same_instance(self, api_key_client):
        stock1 = api_key_client.stock
        stock2 = api_key_client.stock
        assert stock1 is stock2

    def test_stock_with_custom_base_url(self, custom_base_url_client):
        stock = custom_base_url_client.stock
        assert isinstance(stock, RestStockClient)
        assert stock.config['base_url'] == 'https://custom-api.example.com/v2.0/stock'

    def test_stock_and_futopt_different_instances(self, api_key_client):
        stock = api_key_client.stock
        futopt = api_key_client.futopt
        assert stock is not futopt

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

    def test_intraday_quote_custom_base_url(self, mocker, custom_base_url_client):
        stock = custom_base_url_client.stock
        mock_get = mocker.patch('requests.get')
        stock.intraday.quote(symbol='2330')
        mock_get.assert_called_once_with(
            'https://custom-api.example.com/v2.0/stock/intraday/quote/2330',
            headers={'X-API-KEY': 'test-key'}
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

class TestFutOptRestHistoricalClient:
    def test_futopt_historical(self, api_key_client):
        futopt = api_key_client.futopt
        assert hasattr(futopt.historical, 'candles')
        assert hasattr(futopt.historical, 'daily')

    def test_historical_candles_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.historical.candles(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/historical/candles/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_historical_candles_bearer_token(self, bearer_client, mocker):
        futopt = bearer_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.historical.candles(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/historical/candles/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_historical_daily_api_key(self, mocker, api_key_client):
        futopt = api_key_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.historical.daily(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/historical/daily/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_historical_daily_bearer_token(self, bearer_client, mocker):
        futopt = bearer_client.futopt
        mock_get = mocker.patch('requests.get')
        futopt.historical.daily(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/futopt/historical/daily/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )


class TestStockRestTechnicalClient:
    def test_stock_technical(self, api_key_client):
        stock = api_key_client.stock
        assert hasattr(stock.technical, 'sma')
        assert hasattr(stock.technical, 'rsi')
        assert hasattr(stock.technical, 'kdj')
        assert hasattr(stock.technical, 'macd')
        assert hasattr(stock.technical, 'bb')

    def test_technical_sma_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.sma(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/sma/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_technical_sma_bearer_token(self, mocker, bearer_client):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.sma(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/sma/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_technical_rsi_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.rsi(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/rsi/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_technical_rsi_bearer_token(self, mocker, bearer_client):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.rsi(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/rsi/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_technical_kdj_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.kdj(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/kdj/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_technical_kdj_bearer_token(self, mocker, bearer_client):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.kdj(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/kdj/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_technical_macd_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.macd(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/macd/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_technical_macd_bearer_token(self, mocker, bearer_client):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.macd(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/macd/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )

    def test_technical_bb_api_key(self, mocker, api_key_client):
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.bb(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/bb/2330',
            headers={'X-API-KEY': 'api-key'}
        )

    def test_technical_bb_bearer_token(self, mocker, bearer_client):
        stock = bearer_client.stock
        mock_get = mocker.patch('requests.get')
        stock.technical.bb(symbol='2330')
        mock_get.assert_called_once_with(
            'https://api.fugle.tw/marketdata/v1.0/stock/technical/bb/2330',
            headers={'Authorization': 'Bearer bearer-token'}
        )


class TestRestClientFactoryUrlConstruction:
    def test_default_base_url_construction(self, api_key_client):
        # 測試預設 base_url 的 URL 構造
        stock = api_key_client.stock
        assert stock.config['base_url'] == 'https://api.fugle.tw/marketdata/v1.0/stock'
        
        futopt = api_key_client.futopt
        assert futopt.config['base_url'] == 'https://api.fugle.tw/marketdata/v1.0/futopt'

    def test_custom_base_url_construction(self, custom_base_url_client):
        # 測試自訂 base_url 的 URL 構造
        stock = custom_base_url_client.stock
        assert stock.config['base_url'] == 'https://custom-api.example.com/v2.0/stock'
        
        futopt = custom_base_url_client.futopt
        assert futopt.config['base_url'] == 'https://custom-api.example.com/v2.0/futopt'

    def test_url_construction_with_trailing_slash(self):
        # 測試帶有結尾斜線的 base_url，確保沒有雙斜線
        client = RestClient(api_key='test-key', base_url='https://api.example.com/v1/')
        stock = client.stock
        assert stock.config['base_url'] == 'https://api.example.com/v1/stock'

    def test_multiple_clients_independent_base_urls(self):
        # 測試多個客戶端的 base_url 是獨立的
        client1 = RestClient(api_key='key1', base_url='https://api1.example.com')
        client2 = RestClient(api_key='key2', base_url='https://api2.example.com')
        
        stock1 = client1.stock
        stock2 = client2.stock
        
        assert stock1.config['base_url'] == 'https://api1.example.com/stock'
        assert stock2.config['base_url'] == 'https://api2.example.com/stock'


class TestRestClientRegressionTests:
    def test_default_behavior_without_base_url(self, api_key_client):
        # 回歸測試：確保不提供 base_url 時使用預設值
        stock = api_key_client.stock
        assert 'https://api.fugle.tw/marketdata/v1.0/stock' in stock.config['base_url']
        
        futopt = api_key_client.futopt
        assert 'https://api.fugle.tw/marketdata/v1.0/futopt' in futopt.config['base_url']

    def test_api_key_authentication_preserved(self, api_key_client):
        # 回歸測試：確保 API key 認證仍然正常
        stock = api_key_client.stock
        assert stock.config['api_key'] == 'api-key'
        assert 'bearer_token' not in stock.config

    def test_bearer_token_authentication_preserved(self, bearer_client):
        # 回歸測試：確保 Bearer token 認證仍然正常
        stock = bearer_client.stock
        assert stock.config['bearer_token'] == 'bearer-token'
        assert 'api_key' not in stock.config

    def test_existing_api_endpoints_still_work(self, mocker, api_key_client):
        # 回歸測試：確保現有的 API 端點仍然正常工作
        stock = api_key_client.stock
        mock_get = mocker.patch('requests.get')
        
        # 測試幾個主要的 API 端點
        stock.intraday.quote(symbol='2330')
        stock.historical.candles(symbol='2330')
        stock.snapshot.quotes(market='TSE')
        
        # 驗證調用了正確的 URL
        calls = mock_get.call_args_list
        assert len(calls) == 3
        assert 'intraday/quote/2330' in calls[0][0][0]
        assert 'historical/candles/2330' in calls[1][0][0]
        assert 'snapshot/quotes/TSE' in calls[2][0][0]


class TestRestClientUrlNormalization:
    def test_no_trailing_slash_base_url(self):
        # 測試沒有結尾斜線的 base_url
        client = RestClient(api_key='test-key', base_url='https://api.example.com/v1')
        stock = client.stock
        assert stock.config['base_url'] == 'https://api.example.com/v1/stock'
        
    def test_single_trailing_slash_base_url(self):
        # 測試單一結尾斜線的 base_url
        client = RestClient(api_key='test-key', base_url='https://api.example.com/v1/')
        stock = client.stock
        assert stock.config['base_url'] == 'https://api.example.com/v1/stock'
        
    def test_multiple_trailing_slashes_base_url(self):
        # 測試多個結尾斜線的 base_url
        client = RestClient(api_key='test-key', base_url='https://api.example.com/v1///')
        stock = client.stock
        assert stock.config['base_url'] == 'https://api.example.com/v1/stock'
        
    def test_base_url_with_path_and_trailing_slash(self):
        # 測試帶有路徑和結尾斜線的 base_url
        client = RestClient(api_key='test-key', base_url='https://api.example.com/api/v2/')
        stock = client.stock
        assert stock.config['base_url'] == 'https://api.example.com/api/v2/stock'
        futopt = client.futopt
        assert futopt.config['base_url'] == 'https://api.example.com/api/v2/futopt'
