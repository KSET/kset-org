from datetime import datetime

from django.contrib.auth import get_user_model

import factory

from news.models import News
from events.models import Event
from subpages.models import Subpage, Category


__all__ = ['UserFactory', 'NewsFactory', 'EventFactory', 'SubpageCategoryFactory',
    'SubpageFactory']


class UserFactory(factory.django.DjangoModelFactory):
    """
    Generates unique user so other factories don't generate
    integrity error when they need a user.
    """
    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

    FACTORY_FOR = get_user_model()

    username = factory.Sequence(lambda n: 'user%s' % n)
    first_name = factory.Sequence(lambda n: 'Test%s' % n)
    last_name = factory.Sequence(lambda n: 'User%s' % n)
    email = factory.Sequence(lambda n: 'user%s@test.com' % n)
    is_staff = True
    is_active = True
    is_superuser = False


class NewsFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = News

    subject = factory.Sequence(lambda n: 'TestNews%s' % n)
    slug = factory.Sequence(lambda n: 'test-news-%s' % n)


class EventFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Event

    title = factory.Sequence(lambda n: 'TestEvent%s' % n)
    slug = factory.Sequence(lambda n: 'test-event-%s' % n)

    date = datetime.now()
    time = datetime.now()

    content = 'Test Event Content'
    tags = 'test'
    announce = False
    daytime = False
    price = '0kn'
    thumb = None


class SubpageCategoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Category

    name = factory.Sequence(lambda n: 'TestCategory%s' % n)
    slug = factory.Sequence(lambda n: 'test-category-%s' % n)
    parent = None


class SubpageFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Subpage

    title = factory.Sequence(lambda n: 'TestSubpage%s' % n)
    slug = factory.Sequence(lambda n: 'test-subpage-%s' % n)

    description = 'Test Description'
    content = 'Test Content'
    thumb = None
    category = factory.SubFactory(SubpageCategoryFactory)
