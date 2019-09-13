import json
import unittest

from app import create_app


class Base(unittest.TestCase):

    def setUp(self):
        """Prepare testing environment."""

        self.app = create_app('testing')
        self.app = self.app.test_client()

    def test_user_can_get_profile(self):
        """test user can get profile."""
        response = self.app.get('api/v1/profile?username=meshack-mbuvi',
                                content_type='application/json')
        response_data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["followers"], 14)

    def test_returns_404_for_non_existing_user(self):
        """test user can get profile."""
        response = self.app.get('api/v1/profile?username=nfbsjkvdgfk',
                                content_type='application/json')
        print("resdf ", response)
        self.assertEqual(response.status_code, 404)

    def test_requires_username(self):
        """test user can get profile."""
        response = self.app.get('api/v1/profile',
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
