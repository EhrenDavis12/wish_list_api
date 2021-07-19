from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from faker import Faker


class NewUserTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        faker = Faker()
        self.username = faker.user_name()
        self.password = faker.password()
        self.email = faker.email()
        self.firstname = faker.first_name()
        self.lastname = faker.last_name()
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password,
                                             first_name=self.firstname,
                                             last_name=self.lastname)

    def tearDown(self) -> None:
        self.user.delete()


class CreateAndLogInUser:
    def __init__(self):
        self.user = None
        self.user_dict = dict()
        self.login_response = None
        self.access_token = str()

        self.client = APIClient()
        self.create_and_set_user()
        self.login_user()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def create_and_set_user(self) -> None:
        faker = Faker()
        self.user_dict = {'username': faker.user_name(),
                          'password': faker.password(),
                          'email': faker.email(),
                          'firstname': faker.first_name(),
                          'lastname': faker.last_name()}
        self.user = User.objects.create_user(username=self.user_dict['username'],
                                             password=self.user_dict['password'],
                                             first_name=self.user_dict['firstname'],
                                             last_name=self.user_dict['lastname'])

    def login_user(self) -> None:
        self.login_response = self.client.post(
            path='/api/v1/user/login/',
            data={'username': self.user_dict['username'],
                  'password': self.user_dict['password']},
            format='json')
        self.access_token = self.login_response.json()['access']


class LoggedInWithMultiUserTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user1 = CreateAndLogInUser()
        self.user2 = CreateAndLogInUser()

    def tearDown(self) -> None:
        self.user1.client.logout()
        self.user2.client.logout()
        super().tearDown()
