import json
import unittest

import config
from app import create_app, db


class APITestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=config.TestingConfig)
        self.client = self.app.test_client
        self.valid_transaction = {
            'API_KEY': "RANDOM",
            "amount": 100,
            "purchase_desc": "PURCHASE/ Simons ",
            "credit_card": [json.dumps({
                "first_name": "John",
                "last_name": "Doe",
                "number": "356938035643809",
                "cvv": "765",
                "exp_month": 10,
                "exp_year": 22
            })],
            "merchant": [json.dumps({
                "name": "Simons",
                "id": "D84D0C669C3C48779A217CD7C7EC00CC"
            })]
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_index(self):
        """Test index index"""
        res = self.client().get('/', data={})
        self.assertEqual(res.status_code, 200)

    def test_index2(self):
        """ Test index """
        res = self.client().get('/main/index', data={})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Home', str(res.data))

    def test_transaction_without_api_key(self):
        """Test API call without API_KEY"""
        res = self.client().post('/transaction/create', data={})
        self.assertEqual(res.status_code, 401)

    def test_transaction_with_api_key(self):
        """Test API with API_KEY (POST request)."""
        res = self.client().post('/transaction/create', data={'API_KEY': "RANDOM"})
        self.assertEqual(res.status_code, 400)

    # def test_transaction_valid_trasanction(self):
    #     """Test API with API_KEY (POST request)."""
    #     res = self.client().post('/transaction/create', content_type="application/json", data=self.valid_transaction)
    #     self.assertEqual(res.status_code, 200)
