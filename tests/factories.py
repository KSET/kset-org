from datetime import datetime

from django.contrib.auth import get_user_model

import factory

from news.models import News
from events.models import Event
from subpages.models import Subpage, Category
from members.models import Group, Member, MemberGroupLink


__all__ = ['UserFactory', 'NewsFactory', 'EventFactory', 'SubpageCategoryFactory',
    'SubpageFactory', 'MemberFactory', 'GroupFactory', 'MemberGroupLinkFactory']


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


class GroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Group

    name = factory.Sequence(lambda n: 'TestGroup%s' % n)
    slug = factory.Sequence(lambda n: 'test-group-%s' % n)
    parent = None
    description = 'Test Description'


class MemberFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Member

    card_id = factory.Sequence(lambda n: 'CardID-%s' % n)
    name = factory.Sequence(lambda n: 'TestName%s' % n)
    surname = factory.Sequence(lambda n: 'TestSurname%s' % n)
    slug = factory.Sequence(lambda n: 'test-member-%s' % n)
    nickname = factory.Sequence(lambda n: 'TestNickname%s' % n)
    username = factory.Sequence(lambda n: 'testusername%s' % n)
    password = None
    birth = None
    death = None
    comment = None
    image = None


class MemberGroupLinkFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = MemberGroupLink

    member = factory.SubFactory(MemberFactory)
    group = factory.SubFactory(GroupFactory)
    date_start = None
    date_end = None
