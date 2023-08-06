import json

from scanapi.settings import settings

HEADERS = "headers"
BODY = "body"
URL = "url"

SENSITIVE_INFO_SUBSTITUTION_FLAG = "SENSITIVE_INFORMATION"


def hide_sensitive_info(response):
    """ Takes response and begins the hiding of sensitive data process """
    report_settings = settings.get("report", {})
    request = response.request
    request_settings = report_settings.get("hide_request", {})
    response_settings = report_settings.get("hide_response", {})

    _hide(request, request_settings)
    _hide(response, response_settings)


def _hide(http_msg, hide_settings):
    """ Private method that finds all sensitive information attributes and calls _override_info
    to have sensitive data replaced
    """
    for http_attr in hide_settings:
        secret_fields = hide_settings[http_attr]
        for field in secret_fields:
            _override_info(http_msg, http_attr, field)


def _override_info(http_msg, http_attr, secret_field):
    """ Private method that substitutes sensitive data with string 'SENSITIVE_INFORMATION' """

    if http_attr == URL:
        _override_url(http_msg, secret_field)
    elif http_attr == HEADERS:
        _override_headers(http_msg, secret_field)
    elif http_attr == BODY:
        _override_body(http_msg, secret_field)


def _override_url(http_msg, secret_field):
    if secret_field in http_msg.url:
        new_url = http_msg.url.replace(secret_field, SENSITIVE_INFO_SUBSTITUTION_FLAG)
        http_msg.url = new_url


def _override_headers(http_msg, secret_field):
    if secret_field in http_msg.headers:
        http_msg.headers[secret_field] = SENSITIVE_INFO_SUBSTITUTION_FLAG


def _override_body(http_msg, secret_field):
    body = json.loads(http_msg.body.decode("UTF-8"))
    if secret_field in body:
        body[secret_field] = SENSITIVE_INFO_SUBSTITUTION_FLAG
        http_msg.body = json.dumps(body).encode("utf-8")
