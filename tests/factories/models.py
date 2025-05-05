import factory
from faker import Faker
from src.api import models
from nanoid import generate
from datetime import datetime, timezone, timedelta

fake = Faker()


class BaseFactory(factory.Factory):
    class Meta:
        abstract = True

    id = factory.LazyFunction(lambda: generate(size=13))
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class EntityFactory(BaseFactory):
    class Meta:
        abstract = True

    name = factory.LazyFunction(lambda: fake.text(max_nb_chars=3).replace(".", ""))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    description = factory.Faker("paragraph", nb_sentences=5)


class ProjectFactory(EntityFactory):
    class Meta:
        model = models.Project

    start_date = factory.Faker("date_object")

    @factory.lazy_attribute
    def end_date(self):
        return self.start_date + timedelta(days=fake.random_int(min=1, max=365))

    header_url = factory.Faker("image_url")
    cover_url = factory.Faker("image_url")
