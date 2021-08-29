from django.conf import settings
from project.tests.base_test import LoggedInWithMultiUserTestCase, TestUrlMixin



class AppGroupTestUtilsMixin(TestUrlMixin):
    url = 'app_group'

    def get_test_data(self, data={}):
        return {
            "name": self.faker.last_name(),
            "description": self.faker.sentence(),
            "is_active": True,
            **data
        }


class AppGroupMultiUserTestCase(AppGroupTestUtilsMixin, LoggedInWithMultiUserTestCase):
    # fixtures = [f'{settings.BASE_DIR}\\fixtures\\project', f'{settings.BASE_DIR}\\fixtures\\app_user']

    def setUp(self) -> None:
        super().setUp()
        self.user_list = {"users": [self.user1.user, self.user2.user]}
        self.app_group_pk_user1 = "EnxEUqT22S8XUcQd9t8gfZ"
        self.app_group_pk_user2 = "j32KUqnRY6FmnfwFfttc2G"
        self.app_group_pk_user1_and_user2 = "Jag8sSiP2E2PuqeCWWwN4x"

    # def tearDown(self) -> None:
    #     # GroupMember.objects.all().delete()
    #     AppGroup.objects.all().delete()
    #     super().tearDown()


class AppGroupCreateTestCase(AppGroupMultiUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.data = self.get_test_data()

    def test_create(self):
        response = self.create_object(self.user1, self.data)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(self.data['name'], response.data['name'])
        self.assertEquals(self.data['is_active'], response.data['is_active'])
        # Test Creator gets assigned as admin member.
        self.assertEquals(1, response.data['users'].__len__())
        # self.assertEquals(self.user1.user.email, response.data['users'][0]['email'])
        self.assertEquals(self.user1.user.id, response.data['users'][0]["user"])
        self.assertEquals(True, response.data['users'][0]['is_admin'])


class AppGroupReadTestCase(AppGroupMultiUserTestCase):
    def test_listing_user1(self):
        response = self.list_object(self.user1)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(2, response.data['results'].__len__())
        response_names = [x['name'] for x in response.data['results']]
        self.assertTrue('Family' in response_names)
        self.assertTrue('Star Wars' in response_names)

    def test_listing_user2(self):
        response = self.list_object(self.user2)
        response_names = [x['name'] for x in response.data['results']]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(2, response.data['results'].__len__())
        self.assertTrue('AmazingPeople' in response_names)
        self.assertTrue('Family' in response_names)

    def test_retrieve_user1(self):
        pk = 'Jag8sSiP2E2PuqeCWWwN4x'
        response = self.get_object(self.user1, pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(pk, response.data['id'])
        self.assertTrue('Family' in response.data['name'])

    def test_retrieve_as_wrong_user(self):
        pk = self.app_group_pk_user1
        response = self.get_object(self.user2, pk)
        self.assertEquals(response.status_code, 404)


class AppGroupUpdateTestCase(AppGroupMultiUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.pk = self.app_group_pk_user1

    def test_update(self):
        update_data = {'name': 'updated'}
        response = self.update_object(self.user1, update_data, self.pk)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('updated' in response.data['name'])

    def test_update_with_wrong_user(self):
        update_data = {'name': 'bad'}
        response = self.update_object(self.user2, update_data, self.pk)
        self.assertEquals(response.status_code, 404)

    def test_update_add_to_user_list(self):
        update_data = {
            'name': 'newMemberGroup',
            'users': [{"user": self.user1.user.id, "nick_name": "JoneSmthy"}, {"user": self.user2.user.id}],
        }
        response = self.update_object(self.user1, update_data, self.pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(2, response.data['users'].__len__())
        self.assertEquals('newMemberGroup', response.data['name'])

    def test_update_group_user_not_admin(self):
        # user1 is not admin, user2 is
        update_data = {'name': 'bad'}
        response = self.update_object(self.user1, update_data, self.app_group_pk_user1_and_user2)
        self.assertEquals(response.status_code, 400)


class AppGroupDeletedTestCase(AppGroupMultiUserTestCase):
    def test_delete(self):
        response = self.delete_object(self.user1, self.app_group_pk_user1_and_user2)
        self.assertEquals(response.status_code, 204)

        response = self.get_object(self.user1, self.app_group_pk_user1_and_user2)
        self.assertEquals(response.status_code, 404)

    def test_delete_with_wrong_user(self):
        response = self.delete_object(self.user2, self.app_group_pk_user1)
        self.assertEquals(response.status_code, 404)
