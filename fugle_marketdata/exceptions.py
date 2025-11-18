class FugleAPIError(Exception):
    """Fugle API 錯誤，包含 debug 資訊"""

    def __init__(self, message, url=None, status_code=None, params=None, response_text=None):
        self.message = message
        self.url = url
        self.status_code = status_code
        self.params = params
        self.response_text = response_text

        # 建構完整的錯誤訊息
        error_parts = [f"[Fugle API Error] {message}"]
        if url:
            error_parts.append(f"URL: {url}")
        if status_code:
            error_parts.append(f"Status: {status_code}")
        if params:
            error_parts.append(f"Params: {params}")
        if response_text:
            error_parts.append(f"Response: {response_text[:200]}...")

        super().__init__('\n'.join(error_parts))
