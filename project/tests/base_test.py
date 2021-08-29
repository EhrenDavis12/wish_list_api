from django.test import TestCase
from rest_framework.test import APIClient
# from django.contrib.auth.models import User
from app_user.models import User
from faker import Faker


class FindAndLogInUser:
    def __init__(self, user_id):
        self.user = None
        self.login_response = None
        self.access_token = str()

        self.client = APIClient()
        self.user = self.get_user(user_id)
        self.login_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    @staticmethod
    def get_user(user_id) -> User:
        return User.objects.get(pk=user_id)

    def login_user(self) -> None:
        self.login_response = self.client.post(
            path='/api/v1/user/login/',
            data={'username': self.user.username,
                  'password': f"{self.user.first_name}123"},
            format='json')
        self.access_token = self.login_response.json()['access']


class LoggedInWithMultiUserTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user1 = FindAndLogInUser("k6LqwiJKChuj8KNowXE7xk")
        self.user2 = FindAndLogInUser("MzSm82a6jB5xACJ3E6uDZh")
        self.user3 = FindAndLogInUser("D389Dx3MKTPU9zGpcC2R6g")

    def tearDown(self) -> None:
        self.user1.client.logout()
        self.user2.client.logout()
        self.user3.client.logout()
        super().tearDown()


class TestUrlMixin:
    faker = Faker()
    url = None

    @staticmethod
    def get_test_data(data={}):
        return {**data}

    def create_object(self, user, data, url=None):
        url = url or self.url
        return user.client.post(
            path='/api/v1/{0}/'.format(url),
            data=data,
            format='json')

    def list_object(self, user, url=None):
        url = url or self.url
        return user.client.get(
            path='/api/v1/{0}/'.format(url),
            format='json')

    def get_object(self, user, pk, url=None):
        url = url or self.url
        return user.client.get(
            path='/api/v1/{0}/{1}/'.format(url, pk),
            format='json')

    def update_object(self, user, data, pk, url=None):
        url = url or self.url
        return user.client.patch(
            path='/api/v1/{0}/{1}/'.format(url, pk),
            data=data,
            format='json')

    def delete_object(self, user, pk, url=None):
        url = url or self.url
        return user.client.delete(
            path='/api/v1/{0}/{1}/'.format(url, pk),
            format='json')
