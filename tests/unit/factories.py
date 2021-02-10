import factory

from drivr import model
from drivr.model.user import User

factory.Faker._DEFAULT_LOCALE = "pt_BR"

MODULE = "tests.unit.factories"


class UserFactory(factory.Factory):
    class Meta:
        model = model.User

    id = factory.Sequence(lambda n: n)
    email = factory.Faker("email")
    password = factory.Faker("sha1")
    moderator = factory.Faker("boolean")
    active = factory.Faker("boolean")
    created_at = factory.Faker("date_time_between", start_date="-10d")
    updated_at = factory.Faker("date_time_between", start_date="-5d")

    reports = factory.List(
        [
            factory.SubFactory(f"{MODULE}.ReportFactory", user__reports=[])
            for _ in range(5)
        ]
    )


class ReportFactory(factory.Factory):
    class Meta:
        model = model.Report

    id = factory.Sequence(lambda n: n)
    markdown = factory.Faker("paragraph")
    html = factory.Faker("paragraph")
    created_at = factory.Faker("date_time_between", start_date="-10d")
    updated_at = factory.Faker("date_time_between", start_date="-5d")

    user = factory.SubFactory(f"{MODULE}.UserFactory", __sequence=1)
    user_id = factory.LazyAttribute(lambda report: report.user.id)
