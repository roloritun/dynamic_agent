from typing import Any, Dict, Optional

import aiohttp
from openai import BaseModel
import requests
from langchain_community.utilities import Requests



class Requests(BaseModel):
    """Wrapper around requests to handle auth and async.

    The main purpose of this wrapper is to handle authentication (by saving
    headers) and enable easy async methods on the same base object.
    """

    headers: Optional[Dict[str, str]] = None
    aiosession: Optional[aiohttp.ClientSession] = None
    url_params: Optional[Dict[str, str]] = None

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
        extra = "forbid"

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """GET the URL and return the text."""
        if self.url_params:
            url = url + '&'.join([f'{k}={v}' for k, v in self.url_params.items()])
        return requests.get(url, headers=self.headers, **kwargs)

    def post(self, url: str, data: Dict[str, Any], **kwargs: Any) -> requests.Response:
        """POST to the URL and return the text."""
        if self.url_params:
            url = url + '&'.join([f'{k}={v}' for k, v in self.url_params.items()])
        return requests.post(url, json=data, headers=self.headers, **kwargs)

    def patch(self, url: str, data: Dict[str, Any], **kwargs: Any) -> requests.Response:
        """PATCH the URL and return the text."""
        if self.url_params:
            url = url + '&'.join([f'{k}={v}' for k, v in self.url_params.items()])
        return requests.patch(url, json=data, headers=self.headers, **kwargs)

    def put(self, url: str, data: Dict[str, Any], **kwargs: Any) -> requests.Response:
        """PUT the URL and return the text."""
        if self.url_params:
            url = url + '&'.join([f'{k}={v}' for k, v in self.url_params.items()])
        return requests.put(url, json=data, headers=self.headers, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        """DELETE the URL and return the text."""
        if self.url_params:
            url = url + '&'.join([f'{k}={v}' for k, v in self.url_params.items()])
        return requests.delete(url, headers=self.headers, **kwargs)