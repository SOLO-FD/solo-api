import factory
from faker import Faker
from nanoid import generate
from datetime import timedelta  # ,datetime, timezone,

from src.api import domain
from src.api.enums import FileType

fake = Faker()


class BaseDomainFactory(factory.Factory):
    class Meta:
        abstract = True
        model = domain.BaseDomain

    id = factory.LazyFunction(lambda: generate(size=13))
    # created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class EntityDomainFactory(BaseDomainFactory):
    class Meta:
        abstract = True
        model = domain.EntityDomain

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=5).replace(".", ""))
    owner_id = factory.LazyFunction(lambda: generate(size=13))
    # updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    description = factory.Faker("paragraph", nb_sentences=5)


class ProjectDomainFactory(EntityDomainFactory):
    class Meta:
        model = domain.ProjectDomain

    start_date = factory.Faker("date_object")

    @factory.lazy_attribute
    def end_date(self):
        return self.start_date + timedelta(days=fake.random_int(min=1, max=365))

    header_url = factory.Faker("image_url")
    cover_url = factory.Faker("image_url")


class AttachmentDomainFactory(BaseDomainFactory):
    class Meta:
        model = domain.AttachmentDomain

    filename = factory.LazyFunction(lambda: fake.sentence(nb_words=5).replace(".", ""))
    file_type = factory.Faker("enum", enum_cls=FileType)
    url = factory.Faker("url")
    size = factory.Faker("random_int", min=0, max=5000000000)  # ~5GB
    checksum = factory.Faker("sha256")


class TagDomainFactory(EntityDomainFactory):
    class Meta:
        model = domain.TagDomain

    color = factory.Faker("color")
