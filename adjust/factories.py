from factory import fuzzy, Faker
from factory.django import DjangoModelFactory

from adjust.models import PlatformType


class MetricFactory(DjangoModelFactory):
    date = Faker('date')
    country = Faker('country_code')
    channel = Faker('name')
    os = fuzzy.FuzzyChoice(PlatformType.AS_CHOICES)
    impressions = Faker('pyint', min_value=1)
    clicks = Faker('pyint', min_value=1)
    installs = Faker('pyint', min_value=1)
    spend = Faker('pyint', min_value=1)
    revenue = Faker('pyfloat', positive=True)

    class Meta:
        model = 'adjust.Metric'
