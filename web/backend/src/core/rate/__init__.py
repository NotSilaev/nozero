from src.core.rate.policy import THROTTLE_LEVELS

from src.cache import set_cache_value, get_cache_value, MINUTE_SECONDS

from src.utils.common import get_current_datetime, convert_datetime

from fastapi import Request
from fastapi.responses import JSONResponse

import json
from datetime import datetime
from typing import Callable
import functools


class RateManager:
    def __init__(self, request: Request) -> None:
        self.request = request
        
        client_ip: str = self.request.client.host
        self.client_requests_data_cache_key = f"requests-{client_ip}"

        self.request_datetime: datetime = get_current_datetime(timezone_code=None)


    def __set_client_requests_data(self, client_requests_data: dict) -> None:
        serialized_client_requests_data: str = json.dumps(client_requests_data)
        set_cache_value(
            key=self.client_requests_data_cache_key, 
            value=serialized_client_requests_data,
            expire=MINUTE_SECONDS*5
        )


    def __define_client_requests_data(self) -> None:
        """Defines the initial object of data about client requests in the cache."""

        request_path: str = self.request.scope["path"]
        serializable_request_datetime: str = convert_datetime(dt=self.request_datetime, to="str")

        self.__set_client_requests_data(client_requests_data={
            "count": 1, 
            "last": {
                "endpoint": request_path,
                "requested_at": serializable_request_datetime
            },
            "endpoints": {
                request_path: {"count": 1, "last_requested_at": serializable_request_datetime}
            }
        })
        

    def __get_required_delay(self, requests_count: int) -> float:
        """Returns the required delay for accepting a new request based on the number of requests already received."""

        delay = 0

        for level in THROTTLE_LEVELS:
            level_requests, level_delay = level[0], level[1]
            if requests_count >= level_requests:
                delay = level_delay

        return delay


    def get_client_requests_data(self) -> dict:
        """Returns client's requests data from cache."""

        client_requests_data: str | None = get_cache_value(self.client_requests_data_cache_key)
        if client_requests_data:
            return json.loads(client_requests_data)
        return dict()


    def is_request_approved(self) -> bool:
        """Checks the request for exceeding the limit."""

        client_requests_data: dict | None = self.get_client_requests_data()
        if not client_requests_data:
            self.__define_client_requests_data()
            return True
        
        client_requests_count: int = client_requests_data["count"]
        required_delay: float = self.__get_required_delay(requests_count=client_requests_count)

        client_last_request_datetime: datetime = convert_datetime(
            dt=client_requests_data["last"]["requested_at"], 
            to="datetime"
        )
        if (self.request_datetime - client_last_request_datetime).seconds < required_delay:
            return False
        return True
        

    def process_request(self) -> None:
        """Processes the received request and updates the data about the client's requests."""

        request_path: str = self.request.scope["path"]
        serializable_request_datetime: str = convert_datetime(dt=self.request_datetime, to="str")

        client_requests_data: dict = self.get_client_requests_data()
        client_requests_data_endpoints: dict = client_requests_data["endpoints"]
        try:
            client_requests_data_endpoints[request_path]["count"] += 1
            client_requests_data_endpoints[request_path]["last_requested_at"] = serializable_request_datetime
        except KeyError as e:
            print(e)
            client_requests_data_endpoints[request_path] = {
                "count": 1, 
                "last_requested_at": serializable_request_datetime
            }

        self.__set_client_requests_data(client_requests_data={
            "count": client_requests_data["count"] + 1, 
            "last": {
                "endpoint": request_path,
                "requested_at": serializable_request_datetime
            },
            "endpoints": client_requests_data_endpoints
        })


def rate_limiter(max_requests: int, window_seconds: int) -> Callable:
    """Decorator responsible for manually setting the request limit for specific endpoints."""

    def container(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            is_request_approved = True

            request: Request = kwargs["request"]
            if not request:
                is_request_approved = False

            rate_manager = RateManager(request=request)
            client_requests_data: dict = rate_manager.get_client_requests_data()

            request_path: str = request.scope["path"]
            client_endpoint_requests_data: dict = client_requests_data["endpoints"][request_path]

            now: datetime = get_current_datetime(timezone_code=None)
            last_requested_at: datetime = convert_datetime(
                dt=client_endpoint_requests_data["last_requested_at"], 
                to="datetime"
            )

            if (
                (client_endpoint_requests_data["count"]) > max_requests
                and (now - last_requested_at).seconds < window_seconds
            ):
                is_request_approved = False

            if is_request_approved:
                return await func(*args, **kwargs)
            else:
                return JSONResponse(
                    status_code=429,
                    content={
                        "errors": [{
                            "code": "RATE_LIMIT_REACHED",
                            "message": "Too Many Requests"
                        }]
                    }
                )

        return wrapper
    return container
