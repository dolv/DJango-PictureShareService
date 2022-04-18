import os
from dotenv import dotenv_values
from pathlib import Path

from .common import EnvVars
from django.test import TestCase


class QuestionModelTests(TestCase):

    def test_get_value(self):
        """
        EnvVars.get_value() returns None if env var does not exist.
        """
        self.assertIs(EnvVars('develop').get_value('TEST'), None)
