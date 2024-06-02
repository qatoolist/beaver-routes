ALLOWED_COMMON_PARAMS = [
    "url",
    "headers",
    "cookies",
    "auth",
    "timeout",
    "allow_redirects",
    "proxies",
    "verify",
    "stream",
    "cert",
]

ALLOWED_METHOD_PARAMS = {
    "GET": ["params"],
    "POST": ["data", "json", "files"],
    "PUT": ["data", "json", "files"],
    "DELETE": [],
    "PATCH": ["data", "json", "files"],
    "OPTIONS": ["params"],
    "HEAD": ["params"],
}

VALID_HOOK_SCENARIOS = [
    "route",
    "method",
    "scenario",
]

VALID_MERGE_STRATEGIES = [
    "deep_merge",
    "replace",
    "remove",
]
