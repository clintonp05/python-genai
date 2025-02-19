from tenacity import retry, stop_after_attempt, wait_exponential
import httpx
from src.genai.config.settings import AppConfig

class HTTPClient:
    def __init__(self, config: AppConfig):
        self.retry_count = config.http.retry_count
        self.backoff = config.http.retry_backoff
        self.client = httpx.Client()
        self.config = config
        self.retry = retry

    @retry(stop=stop_after_attempt(3), 
          wait=wait_exponential(multiplier=1))
    def execute_request(self, method: str, url: str, **kwargs):
        print(f"Making request to {url}")
        request_headers = kwargs.get('headers', {})
        request_body = kwargs.get('payload', {})
        request_params = kwargs.get('params', {})
        print('request_headers',request_headers)
        print('request_body',request_body)
        print('request_params',request_params)
        self.retry.stop = stop_after_attempt(self.retry_count)
        self.retry.wait = wait_exponential(multiplier=self.backoff)
        # Prepare headers, body, and query parameters

        response = self.client.request(
            method=method,
            url=url,
            headers=request_headers,
            json=request_body,
            params=request_params
        )
        print('response',response)
        print('response',response.content)
        return response