import factory
from faker import Faker
from src.api import models
from nanoid import generate
from datetime import datetime, timezone, timedelta

fake = Faker()


class BaseFactory(factory.Factory):
    class Meta:
        abstract = True
        model = models.BaseModel

    id = factory.LazyFunction(lambda: generate(size=13))
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class EntityFactory(BaseFactory):
    class Meta:
        abstract = True
        model = models.EntityModel

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=5).replace(".", ""))
    owner_id = factory.LazyFunction(lambda: generate(size=13))
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


class AttachmentFactory(BaseFactory):
    class Meta:
        model = models.Attachment

    filename = factory.LazyFunction(lambda: fake.sentence(nb_words=5).replace(".", ""))
    file_type = factory.Faker("enum", enum_cls=models.FileType)
    url = factory.Faker("url")
    size = factory.Faker("random_int", min=0, max=5000000000)  # ~5GB
    checksum = factory.Faker("sha256")
    project = factory.SubFactory(ProjectFactory)
    project_id = factory.SelfAttribute("project.id")


class TagFactory(EntityFactory):
    class Meta:
        model = models.Tag

    color = factory.Faker("color")
