from json import loads

from behave import given, then
from behave.runner import Context
from requests import get


@given("the endpoint {endpoint} is successfully requested")
def step_impl(context: Context, endpoint: str):
    url = f"{context.url_root}{endpoint}"

    context.response = get(url, allow_redirects=True)
    assert (
        context.response.status_code == 200
    ), f"""
    The response HTTP status for a request to {url} is not 200.
    Actual HTTP status: {context.response.status_code}
    """


@then("the JSON response should be")
def step_impl(context: Context):
    expected = loads(context.text)
    actual = context.response.json()

    assert (
        actual == expected
    ), f"""
    The response JSON is different then spected:

    Actual: {actual}
    Expected: {expected}
    """
