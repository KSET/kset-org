import os
from datetime import datetime, timedelta

from django.test import TestCase

from gallery.models import Album, Image, Photographer
from .base import BaseTestClient
from .factories import PhotographerFactory, AlbumFactory, ImageFactory


__all__ = ['GalleryViewTest', 'GalleryTest']


class GalleryViewTest(TestCase):

    def setUp(self):
        super(GalleryViewTest, self).setUp()
        self.client = BaseTestClient()

    def test_gallery_index_page(self):
        ret = self.client.get('gallery_index')
        self.assertEquals(200, ret.status_code)

    def test_list_albums_page(self):
        album = AlbumFactory(category=Album.LIVE)
        ret = self.client.get('gallery_category_albums', category=Album.LIVE)
        self.assertEquals(200, ret.status_code)
        self.assertEquals(1, len(ret.context['albums']))
        self.assertEquals(ret.context['albums'][0].id, album.id)

    def test_list_albums_page_by_category(self):
        album1 = AlbumFactory(category=Album.LIVE)
        album2 = AlbumFactory(category=Album.FOTO)
        ret = self.client.get('gallery_category_albums', category=Album.LIVE)
        self.assertEquals(200, ret.status_code)
        self.assertEquals(1, len(ret.context['albums']))
        self.assertEquals(ret.context['albums'][0].id, album1.id)

        ret = self.client.get('gallery_category_albums', category=Album.FOTO)
        self.assertEquals(200, ret.status_code)
        self.assertEquals(1, len(ret.context['albums']))
        self.assertEquals(ret.context['albums'][0].id, album2.id)

    def test_list_albums_page_by_year(self):
        AlbumFactory(
            category=Album.LIVE,
            date_of_event=(datetime.now() - timedelta(days=800)))
        album = AlbumFactory(
            category=Album.LIVE,
            date_of_event=datetime.now())
        ret = self.client.get(
            'gallery_category_albums_by_year',
            category=Album.LIVE,
            year=datetime.now().year)
        self.assertEquals(200, ret.status_code)
        self.assertEquals(1, len(ret.context['albums']))
        self.assertEquals(ret.context['albums'][0].id, album.id)

    def test_view_album_page(self):
        album = AlbumFactory(
            category=Album.LIVE,
            date_of_event=(datetime.now() - timedelta(days=800)))

        ret = self.client.get(
            'gallery_view_album',
            category=album.category,
            album_slug=album.slug)
        self.assertEquals(200, ret.status_code)

    def test_view_image_page(self):
        album = AlbumFactory()
        image = ImageFactory()
        image.album.add(album)
        ret = self.client.get(
            'gallery_view_image',
            category=album.category,
            album_slug=album.slug,
            image_slug=image.slug)
        self.assertEquals(200, ret.status_code)


class GalleryTest(TestCase):

    def test_saving_an_album_creates_images_and_photographers(self):
        """
        Assert that by creating an album that points to a non empty directory
        of images the images will be parsed and Image objects will be created
        along with Photographer objects. Asserts that we ignore images
        that have filebrowser suffixes.
        """
        import django

        # We need to monkeypatch django's default storage to let us use
        # absolute paths for file fields otherwise it raise an
        # SuspiciousOperation Exception
        def _test_safe_join(base, *paths):
            return os.path.abspath(os.path.join(base, *paths))
        django.core.files.storage.safe_join = _test_safe_join

        album_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'assets', 'test_album')

        album = AlbumFactory(title='test_title1', upload_path=album_path)
        self.assertEquals('test_title1', album.title)
        self.assertEquals(1, Album.objects.all().count())
        self.assertEquals(2, Image.objects.all().count())
        self.assertEquals(1, Photographer.objects.all().count())

        images = Image.objects.all()
        self.assertEquals(images[0].title, '20081222_some_made_up_band_cb_name_surname_01')
        self.assertEquals(images[1].title, '20081222_some_made_up_band_cb_name_surname_02')

        # Test that we don't go and create duplicate Image or
        # Photographer objects on album update
        album.title = 'update_title'
        album.save()

        self.assertEquals(1, Album.objects.all().count())
        self.assertEquals(2, Image.objects.all().count())
        self.assertEquals(1, Photographer.objects.all().count())
