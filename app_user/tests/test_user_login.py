from rest_framework.test import APIClient
from app_user.tests.base_test import NewUserTestCase

class UserLoginTestCase(NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_user_login(self):
        client = APIClient()
        result = client.post(
            path='/api/v1/user/login/',
            data={'username': self.username,
                  'password': self.password},
            format='json')

        self.assertEquals(result.status_code, 200)
        self.assertTrue('access' in result.json())
        self.assertTrue('refresh' in result.json())

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()


class LoginTokenVerifyTestCase(NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_user_login_token_verify(self):
        client = APIClient()
        result_login = client.post(
            path='/api/v1/user/login/',
            data={'username': self.username,
                  'password': self.password},
            format='json')

        result_varify = client.post(
            path='/api/v1/user/token-verify/',
            data={'token': result_login.json()['access']},
            format='json')

        self.assertEquals(result_varify.status_code, 200)

    def tearDown(self) -> None:
        self.client.logout()
        super().tearDown()
