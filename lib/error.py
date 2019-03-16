class CloudflareError(Exception):
    """ Cloudflare Error"""

    def __init__(self, message, extra=None):
        super().__init__(message)
        self.extra = extra


class CloudflareAPIError(CloudflareError):
    """ Cloudflare API error"""
    pass


class CloudflareIPError(CloudflareError):
    """ Occurs when fails to fetch public IP"""
    pass
