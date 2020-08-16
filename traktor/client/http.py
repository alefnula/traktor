import httpx

from traktor.client.errors import (
    HttpClientError,
    HttpClientTimeout,
    HttpRateLimitExceeded,
)


class HttpClient:
    """Generic requests handler.

    Handles retries and HTTP errors.
    """

    ERRORS = {
        401: "Unauthorized",
        403: "Forbidden!",
        404: "Not found.",
        409: "Conflict",
        429: "Under pressure! (Too many requests)",
        500: "You broke it!!!",
        502: "Server not reachable.",
        503: "Server under maintenance.",
    }

    def __init__(
        self, url, token="", timeout=10,
    ):
        """Initialize.

        Args:
            url (str): URL to the SotaBench server.
            token (str): SotaBench authentication token.
            timeout (int): Request timeout time.
        """
        self.url = f"{url.rstrip('/')}/api/v0"
        self.token = token
        self.timeout = timeout

        # Setup headers
        self.headers = {"Content-Type": "application/json"}
        if self.token.strip() != "":
            self.headers["Authorization"] = f"JWT {self.token}"

        self.response = None

    async def request(
        self, method, url, headers=None, params=None, data=None, timeout=None
    ):
        """Request method.

        Request method handles all the url joining, header merging, logging and
        error handling.

        Args:
            method (str): Method for the request - GET or POST
            url (str): Partial url of the request. It is added to the base url
            headers (dict): Dictionary of additional HTTP headers
            params (dict): Dictionary of query parameters for the request
            data (dict): A JSON serializable Python object to send in the body
                of the request. Used only in POST requests.
            timeout (float): How many seconds to wait for the server to send
                data before giving up.
        """
        headers = {**self.headers, **(headers or {})}
        timeout = timeout or self.timeout

        try:
            async with httpx.AsyncClient(
                base_url=self.url, headers=self.headers
            ) as client:
                if method.lower() == "get":
                    self.response = await client.get(
                        url=url,
                        headers=headers,
                        params=params,
                        timeout=timeout,
                    )
                elif method.lower() == "patch":
                    self.response = await client.patch(
                        url=url,
                        headers=headers,
                        params=params,
                        json=data,
                        timeout=timeout,
                    )
                elif method.lower() == "post":
                    self.response = await client.post(
                        url=url,
                        headers=headers,
                        params=params,
                        json=data,
                        timeout=timeout,
                    )
                elif method.lower() == "delete":
                    self.response = await client.delete(
                        url=url,
                        headers=headers,
                        params=params,
                        timeout=timeout,
                    )
                else:
                    raise HttpClientError(f"Unsupported method: {method}")
        except httpx.TimeoutException as e:
            # If request timed out, let upper level handle it they way it sees
            # fit one place might want to retry another might not.
            raise HttpClientTimeout() from e

        except ConnectionError as e:
            raise HttpClientError("Server not reachable.") from e

        except Exception as e:
            raise HttpClientError(f"Unknown error. {e!r}") from e

        if 200 <= self.response.status_code <= 299:
            try:
                return self.response.json() if self.response.text else {}
            except Exception as e:
                raise HttpClientError(
                    f"Error while parsing server response: {e!r}",
                    response=self.response,
                ) from e
        # Check rate limit
        limit = self.response.headers.get("X-Ratelimit-Limit", None)
        if limit is not None:
            remaining = self.response.headers["X-Ratelimit-Remaining"]
            reset = self.response.headers["X-Ratelimit-Reset"]
            retry = self.response.headers["X-Ratelimit-Retry"]

            if remaining == 0:
                raise HttpRateLimitExceeded(
                    response=self.response,
                    limit=limit,
                    remaining=remaining,
                    reset=reset,
                    retry=retry,
                )

        # Try known error messages
        message = self.ERRORS.get(self.response.status_code, None)
        if message is not None:
            raise HttpClientError(message, response=self.response)

        if self.response.status_code == 400:
            try:
                message = "\n".join(self.response.json()["errors"])
            except Exception:
                message = "Bad Request."
            raise HttpClientError(message, response=self.response)

        # Generalize unknown messages.
        try:
            message = self.response.json()["message"]
        except Exception:
            message = "Unknown error."
        raise HttpClientError(message, response=self.response)

    async def get(self, url, headers=None, params=None, timeout=None):
        """Perform get request.

        Args:
            url (str): Partial url of the request. It is added to the base url
            headers (dict): Dictionary of additional HTTP headers
            params (dict): Dictionary of query parameters for the request
            timeout (float): How many seconds to wait for the server to send
                data before giving up

        Returns:
            dict: Deserialized json response.

        """
        return await self.request(
            method="get",
            url=url,
            headers=headers,
            params=params,
            timeout=timeout,
        )

    async def patch(
        self, url, headers=None, params=None, data=None, timeout=None
    ):
        """Perform patch request.

        Args:
            url (str): Partial url of the request. It is added to the base url
            headers (dict): Dictionary of additional HTTP headers
            params (dict): Dictionary of query parameters for the request
            data (dict): A JSON serializable Python object to send in the body
                of the request.
            timeout (float): How many seconds to wait for the server to send
                data before giving up

        Returns:
            dict: Deserialized json response.

        """
        return await self.request(
            method="patch",
            url=url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
        )

    async def post(
        self, url, headers=None, params=None, data=None, timeout=None
    ):
        """Perform post request.

        Args:
            url (str): Partial url of the request. It is added to the base url
            headers (dict): Dictionary of additional HTTP headers
            params (dict): Dictionary of query parameters for the request
            data (dict): A JSON serializable Python object to send in the body
                of the request.
            timeout (float): How many seconds to wait for the server to send
                data before giving up

        Returns:
            dict: Deserialized json response.

        """
        return await self.request(
            method="post",
            url=url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
        )

    async def delete(self, url, headers=None, params=None, timeout=None):
        """Perform delete request.

        Args:
            url (str): Partial url of the request. It is added to the base url
            headers (dict): Dictionary of additional HTTP headers
            params (dict): Dictionary of query parameters for the request
            timeout (float): How many seconds to wait for the server to send
                data before giving up

        Returns:
            dict: Deserialized json response.
        """
        return await self.request(
            method="delete",
            url=url,
            headers=headers,
            params=params,
            timeout=timeout,
        )
