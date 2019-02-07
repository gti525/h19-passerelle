
# test_bucketlist.py
import unittest
import os
import json
from app import create_app, db
import config

class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=config.TestingConfig)
        self.client = self.app.test_client
        self.transaction = {'name': 'Go to Borabora for vacation'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    # def test_bucketlist_creation(self):
    #     """Test API can create a bucketlist (POST request)"""
    #     res = self.client().post('/api/transactions', data=self.bucketlist)
    #     self.assertEqual(res.status_code, 201)
    #     self.assertIn('Go to Borabora', str(res.data))
    #
    # def test_api_can_get_all_bucketlists(self):
    #     """Test API can get a bucketlist (GET request)."""
    #     res = self.client().post('/bucketlists/', data=self.bucketlist)
    #     self.assertEqual(res.status_code, 201)
    #     res = self.client().get('/bucketlists/')
    #     self.assertEqual(res.status_code, 200)
    #     self.assertIn('Go to Borabora', str(res.data))