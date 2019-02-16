from unittest import TestCase

from app import create_app
from config import TestingConfig, DevelopmentConfig, StagingConfig

import pytest
import os

basedir = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestingConfig)
    return app


def test_dev_settings(app):
    app.config.from_object(DevelopmentConfig)
    assert app.config["DEBUG"]
    assert app.config["DEVELOPMENT"]


def test_testing_settings(app):
    app.config.from_object(TestingConfig)
    assert app.config["TESTING"]

    assert app.config["SQLALCHEMY_DATABASE_URI"] == TestingConfig.SQLALCHEMY_DATABASE_URI
