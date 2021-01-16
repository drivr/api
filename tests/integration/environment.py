from behave import use_fixture
from behave.model import Scenario
from behave.runner import Context

from tests.integration.helpers import fixtures


def before_all(context: Context):
    use_fixture(fixtures.setup_app, context)


def before_scenario(context: Context, scenario: Scenario):
    use_fixture(fixtures.setup_db, context)
