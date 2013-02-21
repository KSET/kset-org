from django.contrib.syndication.views import Feed
# from django.contrib.syndication.feeds import Feed
from events.models import Event
from django.utils.feedgenerator import Atom1Feed

import datetime


class RssProgramFeed(Feed):
    title = "www.KSET.org"
    link = "http://www.kset.org/"
    description = "Klub Studenata ElektroTehnike - Program"
    description_template = "templates/feed_description.html"

    def item_pubdate(self, obj):
        if (obj.time):
            return datetime.datetime(obj.date.year, obj.date.month, obj.date.day,
                obj.time.hour, obj.time.minute)
        else:
            return datetime.datetime(obj.date.year, obj.date.month, obj.date.day)

    def items(self):
        return Event.objects.get_forward()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description + item.content


class AtomProgramFeed(RssProgramFeed):
    feed_type = Atom1Feed
    subtitle = RssProgramFeed.description
