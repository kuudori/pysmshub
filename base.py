class BaseSmsHubApi:
    """Base SmsHub API class, shared logic goes here."""

    def __init__(self, apikey: str, proxy=None):
        self.api_key = apikey
        self.base_url = "http://smshub.org/stubs/handler_api.php"
        self.proxy = proxy
        self.proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
