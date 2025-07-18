import pytest
import requests
from unittest.mock import Mock, patch
from fugle_marketdata.rest.base_rest import BaseRest


class TestBaseRest:
    """測試 BaseRest 類別的功能"""
    
    @pytest.fixture
    def base_rest_with_api_key(self):
        """建立使用 API Key 的 BaseRest 實例"""
        return BaseRest(
            base_url="https://api.fugle.tw/marketdata/v1.0",
            api_key="test-api-key"
        )
    
    @pytest.fixture
    def base_rest_with_bearer_token(self):
        """建立使用 Bearer Token 的 BaseRest 實例"""
        return BaseRest(
            base_url="https://api.fugle.tw/marketdata/v1.0",
            bearer_token="test-bearer-token"
        )
    
    @pytest.fixture
    def base_rest_no_auth(self):
        """建立沒有驗證的 BaseRest 實例"""
        return BaseRest(
            base_url="https://api.fugle.tw/marketdata/v1.0"
        )

    def test_successful_json_response(self, base_rest_with_api_key):
        """測試成功的 JSON 回應"""
        expected_data = {"status": "success", "data": [1, 2, 3]}
        
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = expected_data
            mock_get.return_value = mock_response
            
            result = base_rest_with_api_key.request("/test")
            
            assert result == expected_data
            mock_get.assert_called_once_with(
                "https://api.fugle.tw/marketdata/v1.0/test",
                headers={"X-API-KEY": "test-api-key"}
            )

    def test_invalid_json_response_raises_exception(self, base_rest_with_api_key):
        """測試無效的 JSON 回應會拋出異常"""
        invalid_response_text = "<html><body>Server Error</body></html>"
        
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("No JSON object could be decoded")
            mock_response.text = invalid_response_text
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/test")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)

    def test_json_decode_error_with_different_error_types(self, base_rest_with_api_key):
        """測試不同類型的 JSON 解碼錯誤"""
        response_text = "This is not JSON"
        
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("Expecting "," delimiter")
            mock_response.text = response_text
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/test")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)

    def test_empty_response_text_in_error(self, base_rest_with_api_key):
        """測試空的回應內容時的錯誤處理"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("No JSON object could be decoded")
            mock_response.text = ""
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/test")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)

    def test_real_world_error_scenarios(self, base_rest_with_api_key):
        """測試真實世界的錯誤情境"""
        html_response = "<!DOCTYPE html><html><head><title>500 Internal Server Error</title></head><body><h1>Internal Server Error</h1></body></html>"
        
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("No JSON object could be decoded")
            mock_response.text = html_response
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/test")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)

    def test_partial_json_response_error(self, base_rest_with_api_key):
        """測試部分 JSON 回應錯誤"""
        partial_json = '{"status": "success", "data": ['
        
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("Unterminated string")
            mock_response.text = partial_json
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/test")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)

    def test_integration_with_stock_client(self, base_rest_with_api_key):
        """測試與 Stock Client 的集成"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_response.text = "<html>Error Page</html>"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/stock/intraday/quote/2330")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)

    def test_json_content_type_mismatch(self, base_rest_with_api_key):
        """測試當伺服器回傳非 JSON 內容類型時的處理"""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("No JSON object could be decoded")
            mock_response.text = "<xml><error>Service unavailable</error></xml>"
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/test")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)

    def test_network_timeout_with_partial_response(self, base_rest_with_api_key):
        """測試網路超時導致的部分回應"""  
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = ValueError("Expecting property name enclosed in double quotes")
            mock_response.text = '{"data": {"price": 150.0, "volume":'
            mock_get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                base_rest_with_api_key.request("/stock/quote/2330")
            
            assert "An unexpected data error occurred.\nPlease try again later. If the issue persists, please contact support at  (tech.support@fugle.tw)" in str(exc_info.value)
