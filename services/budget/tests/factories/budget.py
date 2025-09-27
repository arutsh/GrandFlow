import factory
from app.models.budget_model import BudgetModel


class BudgetFactory(factory.Factory):
    class Meta:
        model = BudgetModel

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("word")
    owner_id = factory.Faker("uuid4")
    funding_customer_id = factory.Faker("uuid4")
    external_funder_name = factory.Faker("company")
