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

    @patch('src.application.requests.post')
    def test_rejestracja(self, mock_post):
        create_request_mock(mock_post, FakeResponse(201, {'id': 1}))
        response = self.app.rejestracja('91230303040', 'testowanie', 'haslo1234')
        assert_that(response.json['id']).is_greater_than(0)

    @patch('src.application.requests.post')
    def test_rejestracja_mock_post(self, mock_post):
        create_request_mock(mock_post, FakeResponse(201, {'id': 1}))
        self.app.rejestracja('01230902964', 'login', 'haslo', )
        mock_post.assert_called_once()

    def test_rejestracja_zly_typ(self):
        assert_that(self.app.rejestracja).raises(
            TypeError).when_called_with('string')

    @patch('src.application.requests.post')
    def test_rejestracja_istniejace_konto(self, mock_post):
        create_request_mock(mock_post, FakeResponse(409))
        response = self.app.rejestracja('01230902964', 'login', 'haslo')
        assert_that(response).is_equal_to('Podany użytkownik już istnieje')

    @patch('src.application.requests.post')
    def test_rejestracja_inne_bledy_mock(self, mock_post):
        create_request_mock(mock_post, FakeResponse(404,
                                                    error_message='Blad'))
        self.app.rejestracja('01230902964', 'login', 'haslo')
        mock_post.assert_called_once()

    def test_rejestracja_haslo_int(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('peselpeslelp', 'login', 1)

    def test_rejestracja_pesel_int(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with(1, 'login', 'haslo')