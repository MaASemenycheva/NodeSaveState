# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from nodesavestate.models import State


class StateViewTestCase(APITestCase):
    url_reverse = reverse('api:state-list')
    url = '/api/state/'
    url_detail = '/api/state/{}/'
    url_detail_route_reverse = reverse('api:state-detail', kwargs={"pk": 1})
    url_detail_route = '/api/state/{}/detail/'
    url_list_route = '/api/state/all_chat_id/'

    def setUp(self):
        print('setUp')

        self.client = APIClient()
        # create user
        User.objects.create_user(username='test_user', password='password123')

        self.client.login(username='test_user', password='password123')

        self.request_data = {
            'chat_id': 'chat_id_test',
            'node_id': 'node_id_test'
        }

        self.music = State.objects.create(song='chat_id_test', singer='node_id_test')

    def test_api_state_create(self):
        print('test_api_state_create')
        self.response = self.client.post(
            self.url,
            self.request_data,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(State.objects.count(), 2)
        self.assertEqual(State.objects.get(pk=self.state.id).chat_id, 'chat_id_test')
        self.assertEqual(State.objects.get(pk=self.state.id).node_id, 'node_id_test')

    def test_api_state_retrieve(self):
        print('test_api_state_retrieve')
        state = State.objects.get(pk=self.music.id)
        response = self.client.get(self.url_detail.format(self.music.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('chat_id', None), state.chat_id)
        self.assertEqual(response.data.get('node_id', None), state.node_id)

    def test_api_state_partial_update(self):
        print('test_api_state_partial_update')
        update_chat_id = {'chat_id': 'chat_id_update'}
        response = self.client.patch(self.url_detail.format(self.state.id), update_chat_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('chat_id', None), update_chat_id.get('chat_id', None))

    def test_api_state_update(self):
        print('test_api_state_update')
        update_chat_id = {'chat_id': 'chat_id_update', 'node_id': 'node_id_update'}
        response = self.client.put(self.url_detail.format(self.state.id), update_chat_id, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('chat_id', None), update_chat_id.get('chat_id'))
        self.assertEqual(response.data.get('node_id', None), update_chat_id.get('node_id'))

    def test_api_state_delete(self):
        print('test_api_state_delete')
        response = self.client.delete(self.url_detail.format(self.state.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_music_detail_route(self):
        print('test_api_status_detail_route')
        state = State.objects.get(pk=self.music.id)
        response = self.client.get(self.url_detail_route.format(self.music.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('chat_id', None), state.chat_id)
        self.assertEqual(response.data.get('node_id', None), state.node_id)

    def test_api_music_list_route(self):
        print('test_api_music_list_route')
        state = State.objects.values_list('node_id', flat=True).distinct()
        response = self.client.get(self.url_list_route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(next(iter(response.data)), next(iter(state)))