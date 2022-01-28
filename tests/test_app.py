import unittest
from unittest.mock import *
from src.application import *
from assertpy import assert_that
import io


def create_request_mock(to_mock, fake_response):
    to_mock.return_value = Mock(ok=True)
    to_mock.return_value = fake_response


class ZalogujSieTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = ZalogujSie()