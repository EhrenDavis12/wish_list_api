from faker import Faker

from project.tests.base_test import LoggedInWithMultiUserTestCase
from project.models import WishList


class WishListTestUtilsMixin:
    @staticmethod
    def get_test_data():
        faker = Faker()
        return {'name': faker.last_name()}

    @staticmethod
    def create_wish_list( user, data):
        return user.client.post(
            path='/api/v1/wishlist/',
            data=data,
            format='json')

    @staticmethod
    def list_wish_list(user):
        return user.client.get(
            path='/api/v1/wishlist/',
            format='json')

    @staticmethod
    def get_wish_list(user, pk):
        return user.client.get(
            path='/api/v1/wishlist/' + pk + '/',
            format='json')

    @staticmethod
    def update_wish_list(user, data, pk):
        return user.client.patch(
            path='/api/v1/wishlist/'+pk+'/',
            data=data,
            format='json')

    @staticmethod
    def delete_wish_list(user, pk):
        return user.client.delete(
            path='/api/v1/wishlist/' + pk + '/',
            format='json')


class WishListMultiUserTestCase(WishListTestUtilsMixin, LoggedInWithMultiUserTestCase):
    def tearDown(self) -> None:
        WishList.objects.all().delete()
        super().tearDown()


class WishListCreateTestCase(WishListMultiUserTestCase):
    def test_create(self):
        data = self.get_test_data()
        response = self.create_wish_list(self.user1, data)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(data['name'] in response.data['data']['name'])


class WishListReadTestCase(WishListMultiUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.data1 = self.get_test_data()
        self.data2 = self.get_test_data()
        self.data3 = self.get_test_data()
        self.wish_list1 = self.create_wish_list(self.user1, self.data1)
        self.wish_list2 = self.create_wish_list(self.user2, self.data2)
        self.wish_list3 = self.create_wish_list(self.user2, self.data3)

    def test_listing_user1(self):
        response = self.list_wish_list(self.user1)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(1, response.data.__len__())
        self.assertTrue(self.data1['name'] in response.data[0]['name'])

    def test_listing_user2(self):
        response = self.list_wish_list(self.user2)
        name = [x['name'] for x in response.data]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(2, response.data.__len__())
        self.assertTrue(self.data2['name'] in name)
        self.assertTrue(self.data3['name'] in name)

    def test_retrieve_user1(self):
        pk = self.wish_list1.data['data']['id']
        response = self.get_wish_list(self.user1, pk)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(pk, response.data['id'])
        self.assertTrue(self.data1['name'] in response.data['name'])

    def test_retrieve_as_wrong_user(self):
        pk = self.wish_list1.data['data']['id']
        response = self.get_wish_list(self.user2, pk)
        self.assertEquals(response.status_code, 404)


class WishListUpdateTestCase(WishListMultiUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.data = self.get_test_data()
        self.wish_list = self.create_wish_list(self.user1, self.data)
        self.pk = self.wish_list.data['data']['id']

    def test_update(self):
        update_data = {'name': 'updated'}
        response = self.update_wish_list(self.user1, update_data, self.pk)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('updated' in response.data['data']['name'])

    def test_update_with_wrong_user(self):
        update_data = {'name': 'bad'}
        response = self.update_wish_list(self.user2, update_data, self.pk)
        self.assertEquals(response.status_code, 404)


class WishListDeletedTestCase(WishListMultiUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.data1 = self.get_test_data()
        self.data2 = self.get_test_data()
        self.wish_list1 = self.create_wish_list(self.user1, self.data1)
        self.wish_list2 = self.create_wish_list(self.user1, self.data2)
        self.pk1 = self.wish_list1.data['data']['id']
        self.pk2 = self.wish_list2.data['data']['id']

    def test_delete(self):
        response = self.delete_wish_list(self.user1, self.pk1)
        self.assertEquals(response.status_code, 200)

        response = self.get_wish_list(self.user1, self.pk1)
        self.assertEquals(response.status_code, 404)

    def test_delete_with_wrong_user(self):
        response = self.delete_wish_list(self.user2, self.pk2)
        self.assertEquals(response.status_code, 404)
