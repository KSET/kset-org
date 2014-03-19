from django.test import TestCase

from members.forms import LoginForm
from members.models import ResetPasswordLink
from .base import BaseTestClient
from .factories import MemberFactory, UserFactory, MemberContactFactory


__all__ = ['MembersViewTest']


class MembersViewTest(TestCase):

    def setUp(self):
        super(MembersViewTest, self).setUp()
        self.client = BaseTestClient()

    def test_loging_in_successfully(self):
        member = MemberFactory(username='test')
        member.set_password('test')
        member.save()
        form = LoginForm({
            'username': 'test',
            'password': 'test'})
        self.assertTrue(form.is_valid())

    def test_login_fail_wrong_password(self):
        member = MemberFactory(username='test')
        member.set_password('test')
        member.save()
        form = LoginForm({
            'username': 'test',
            'password': 'WRONG_PASSWORD'})
        self.assertFalse(form.is_valid())

    def test_login_fail_password_not_set(self):
        member = MemberFactory(username='test')
        member.set_password('test')
        member.save()
        form = LoginForm({
            'username': 'test',
            'password': None})
        self.assertFalse(form.is_valid())

    def test_main_page_without_login(self):
        ret = self.client.get('members_index')
        self.assertEquals(302, ret.status_code)

    def test_main_page_with_login(self):
        member = MemberFactory(username='test')
        member.set_password('test')
        member.save()
        self.client.post('members_login', data={'username': 'test', 'password': 'test'})
        ret = self.client.get('members_index')
        self.assertEquals(200, ret.status_code)
        self.assertEquals(ret.context['member'], member)

    def test_members_logout(self):
        member = MemberFactory(username='test')
        member.set_password('test')
        member.save()
        self.client.post('members_login', data={'username': 'test', 'password': 'test'})
        ret = self.client.get('members_index')
        self.assertEquals(200, ret.status_code)

        self.client.get('members_logout')
        ret = self.client.get('members_index')
        self.assertEquals(302, ret.status_code)

    def test_list_all_page_without_login(self):
        ret = self.client.get('members_list_all')
        self.assertEquals(302, ret.status_code)

    def test_list_all_page_with_login(self):
        member = MemberFactory(username='test')
        member.set_password('test')
        member.save()
        self.client.post('members_login', data={'username': 'test', 'password': 'test'})
        ret = self.client.get('members_list_all')
        self.assertEquals(200, ret.status_code)
        self.assertIsNotNone(ret.context['members'])

    def test_get_profile_without_login(self):
        member = MemberFactory(username='test')
        ret = self.client.get('members_get_member', id=member.id)
        self.assertEquals(302, ret.status_code)

    def test_get_profile_with_login(self):
        member = MemberFactory(username='test')
        member.set_password('test')
        member.save()
        self.client.post('members_login', data={'username': 'test', 'password': 'test'})
        ret = self.client.get('members_get_member', id=member.id)
        self.assertEquals(200, ret.status_code)
        self.assertEquals(ret.context['member'], member)

    def test_red_table_page_without_login(self):
        """
        Red table page requires a django.contrib.auth.User to be logged in
        """
        ret = self.client.get('members_red_table')
        self.assertEquals(302, ret.status_code)

    def test_red_table_page_with_login(self):
        UserFactory(username='test', password='test')
        self.client.login(username='test', password='test')
        ret = self.client.get('members_red_table')
        self.assertEquals(200, ret.status_code)

    def test_red_list_page_without_login(self):
        """
        Red list page requires a django.contrib.auth.User to be logged in
        """
        ret = self.client.get('members_red_list')
        self.assertEquals(302, ret.status_code)

    def test_forgot_password_form(self):
        member = MemberFactory(username='test')
        email = MemberContactFactory(member=member, contact='me@kset.org')

        response = self.client.post('members_forgot_password', {'email': email.contact})
        self.assertEquals(302, response.status_code)
        self.assertEquals(1, ResetPasswordLink.objects.all().count())

    def test_forgot_password_form_only_one_reset_link_per_user(self):
        member = MemberFactory(username='test')
        email = MemberContactFactory(member=member, contact='me@kset.org')

        response = self.client.post('members_forgot_password', {'email': email.contact})
        # and again
        response = self.client.post('members_forgot_password', {'email': email.contact})
        self.assertEquals(302, response.status_code)
        self.assertEquals(1, ResetPasswordLink.objects.all().count())

    def test_forgot_password_form_invalid_email(self):
        response = self.client.post('members_forgot_password', {'email': 'email@email.com'})
        # 200 because the form will just re-render with errors
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, ResetPasswordLink.objects.all().count())
