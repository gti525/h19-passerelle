import json
import unittest

import config
from app import create_app, db


class APITestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

