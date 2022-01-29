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

    def test_rejestracja_login_int(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('peselpesell' , 1 , 'haslo')

    def test_rejestracja_haslo_float(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('peselpeslelp','login', 1.3)

    def test_rejestracja_pesel_float(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with(1.7 , 'login', 'haslo')

    def test_rejestracja_login_float(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('peselpesell' , 1.8 , 'haslo')

    def test_rejestracja_haslo_puste(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('peselpeslelp', 'login', '')

    def test_rejestracja_pesel_pusty(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('', 'login', 'haslo')

    def test_rejestracja_login_pusty(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('peselpesell' , '' , 'haslo')

    def test_rejestracja_pesel_za_krotki(self):
        assert_that(self.app.rejestracja).raises(
            ValueError).when_called_with('pessell', 'login', 'haslo')

    def test_login_login_int(self):
        assert_that(self.app.login).raises(
            ValueError).when_called_with(1, 'haslo')

    def test_login_login_float(self):
        assert_that(self.app.login).raises(
            ValueError).when_called_with(3.6, 'haslo')

    def test_login_haslo_int(self):
        assert_that(self.app.login).raises(
            ValueError).when_called_with('login', 1)

    def test_login_haslo_float(self):
        assert_that(self.app.login).raises(
            ValueError).when_called_with('login', 1.4)

    def test_login_haslo_puste(self):
        assert_that(self.app.login).raises(
            ValueError).when_called_with('login', '')

    def test_login_login_pusty(self):
        assert_that(self.app.login).raises(
            ValueError).when_called_with('', 'haslo')

    @patch('src.application.requests.delete')
    def test_usuwanie_istnieje(self, mock_delete):
        create_request_mock(mock_delete, FakeResponse(200, {'deleted': 'julia'}))
        response = self.app.usun('julia')
        assert_that(response.json['deleted']).is_equal_to('julia')

    @patch('src.application.requests.delete')
    def test_usuwanie_istnieje_mock(self, mock_delete):
        create_request_mock(mock_delete, FakeResponse(200))
        self.app.usun('login')
        mock_delete.assert_called_once()

    def test_usuwanie_zly_typ_danych(self):
        assert_that(self.app.usun).raises(
            TypeError).when_called_with('haslo', 'jdjd')

    def test_usuwanie_nie_istnieje(self):
        self.app.usun = MagicMock(
            return_value=FakeResponse(404, error_message= "Nie znaleziono użytkownika"))
        response = self.app.usun()
        assert_that(response.error_message).contains('Nie', 'znaleziono')

    def test_usuwanie_nie_istnieje_mock(self):
        self.app.usun = MagicMock(
            return_value=FakeResponse(404, error_message= "Nie znaleziono użytkownika"))
        self.app.usun()
        self.app.usun.assert_called_with()


    def test_usuwanie_server_error(self):
        self.app.usun = MagicMock(side_effect=ConnectionError(
            'Ups... Coś poszło nie tak'))
        assert_that(self.app.usun).raises(
            ConnectionError).when_called_with()

    def test_usun_login_int(self):
        assert_that(self.app.usun).raises(
            ValueError).when_called_with(1)

    def test_usun_login_float(self):
        assert_that(self.app.usun).raises(
            ValueError).when_called_with(1.5)

    def test_usun_login_pusty(self):
        assert_that(self.app.usun).raises(
            ValueError).when_called_with('')

    @patch('src.application.requests.put')
    def test_edycja_pesel(self, mock_put):
        create_request_mock(mock_put, FakeResponse(201,
                                                   {'pesel': 'pesel'}))
        response = self.app.edycja_pesel('peselpeselp')
        assert_that(response.json['pesel']).is_equal_to('pesel')

    @patch('src.application.requests.put')
    def test_edycja_pesel_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(200, {'pesel': 'pesel'}))
        self.app.edycja_pesel('peselpeselp')
        mock_put.assert_called_once()

    def test_edycja_pesel_zly_typ(self):
        assert_that(self.app.edycja_pesel).raises(
            TypeError).when_called_with('integer', {'pesel': 'pesel'})

    def test_edycja_pesel_zly_typ_2(self):
        assert_that(self.app.edycja_pesel).raises(
            TypeError).when_called_with(2, 'object')

    def test_edycja_pesel_brak_Wartosci(self):
        assert_that(self.app.edycja_pesel).raises(
            ValueError).when_called_with('')

    @patch('src.application.requests.put')
    def test_edycja_pesel_pesel_istnieje(self, mock_put):
        create_request_mock(mock_put, FakeResponse(409,
                                                   error_message='Taki pesel juz istnieje'))
        response = self.app.edycja_login('pesel')
        assert_that(response).is_equal_to('Ups... Coś poszło nie tak')

    def test_edycja_pesel_istnieje_mock(self):
        self.app.update = Mock()
        self.app.update.return_value = FakeResponse(409,
                                                            error_message='Pesel istnieje')
        self.app.update(1, {'pesel':'pesel'})
        self.app.update.assert_called_once()

    @patch('src.application.requests.put')
    def test_edycja_pesel_nie_istnieje(self, mock_put):
        create_request_mock(mock_put, FakeResponse(404,
                                                   error_message='nie znaleziono uzytkownika'))
        response = self.app.edycja_pesel('peselpeselp')
        assert_that(response).contains('Ups', 'nie')

    @patch('src.application.requests.put')
    def test_pesel_nie_istnieje_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(404,
                                                   error_message='nie znaleziono użytkownika'))
        self.app.edycja_pesel('peselpeselp')
        mock_put.assert_called_once()

    @patch('src.application.requests.put')
    def test_edycja_pesel_inne_bledy(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        response = self.app.edycja_pesel('peselpeselp')
        assert_that(response).is_equal_to_ignoring_case('Ups... Coś poszło nie tak')

    @patch('src.application.requests.put')
    def test_edycja_pesel_inne_bledy_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        self.app.edycja_pesel('peselpeselp')
        mock_put.assert_called_once()

    def test_edycja_pesel_pesel_pusty(self):
        assert_that(self.app.edycja_pesel).raises(
            ValueError).when_called_with('')

    def test_edycja_pesel_pesel_int(self):
        assert_that(self.app.edycja_pesel).raises(
            ValueError).when_called_with(1)

    def test_edycja_pesel_pesel_float(self):
        assert_that(self.app.edycja_pesel).raises(
            ValueError).when_called_with(1.7)

    @patch('src.application.requests.put')
    def test_edycja_login(self, mock_put):
        create_request_mock(mock_put, FakeResponse(201,
                                                   {'login': 'login'}))
        response = self.app.edycja_login('login')
        assert_that(response.json['login']).is_equal_to('login')

    @patch('src.application.requests.put')
    def test_edycja_login_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(200, {'login': 'login'}))
        self.app.edycja_login('login')
        mock_put.assert_called_once()

    def test_edycja_login_zly_typ(self):
        assert_that(self.app.edycja_login).raises(
            TypeError).when_called_with('integer', {'login': 'login'})

    def test_edycja_login_zly_typ_2(self):
        assert_that(self.app.edycja_login).raises(
            TypeError).when_called_with(2, 'object')

    def test_edycja_login_brak_Wartosci(self):
        assert_that(self.app.edycja_login).raises(
            ValueError).when_called_with('')

    @patch('src.application.requests.put')
    def test_edycja_login_login_istnieje(self, mock_put):
        create_request_mock(mock_put, FakeResponse(409,
                                                   error_message='Taki login juz istnieje'))
        response = self.app.edycja_login('login')
        assert_that(response).is_equal_to('Ups... Coś poszło nie tak')

    def test_edycja_login_istnieje_mock(self):
        self.app.update = Mock()
        self.app.update.return_value = FakeResponse(409,
                                                    error_message='Login istnieje')
        self.app.update(1, {'login': 'login'})
        self.app.update.assert_called_once()

    @patch('src.application.requests.put')
    def test_edycja_uzytkownik_nie_istnieje(self, mock_put):
        create_request_mock(mock_put, FakeResponse(404,
                                                   error_message='nie znaleziono uzytkownika'))
        response = self.app.edycja_login('login')
        assert_that(response).contains('Ups', 'nie')

    @patch('src.application.requests.put')
    def test_uzytkownik_nie_istnieje_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(404,
                                                   error_message='nie znaleziono użytkownika'))
        self.app.edycja_login('login')
        mock_put.assert_called_once()

    @patch('src.application.requests.put')
    def test_edycja_login_inne_bledy(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        response = self.app.edycja_login('login')
        assert_that(response).is_equal_to_ignoring_case('Ups... Coś poszło nie tak')

    @patch('src.application.requests.put')
    def test_edycja_login_inne_bledy_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        self.app.edycja_login('login')
        mock_put.assert_called_once()

    def test_edycja_login_login_pusty(self):
        assert_that(self.app.edycja_login).raises(
            ValueError).when_called_with('')

    def test_edycja_login_login_int(self):
        assert_that(self.app.edycja_login).raises(
            ValueError).when_called_with(1)

    def test_edycja_login_login_float(self):
        assert_that(self.app.edycja_login).raises(
            ValueError).when_called_with(1.7)

    @patch('src.application.requests.put')
    def test_edycja_haslo(self, mock_put):
        create_request_mock(mock_put, FakeResponse(201,
                                                   {'haslo': 'haslo'}))
        response = self.app.edycja_haslo('haslo')
        assert_that(response.json['haslo']).is_equal_to('haslo')

    @patch('src.application.requests.put')
    def test_edycja_haslo_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(200, {'haslo': 'haslo'}))
        self.app.edycja_haslo('haslo')
        mock_put.assert_called_once()

    def test_edycja_haslo_zly_typ(self):
        assert_that(self.app.edycja_haslo).raises(
            TypeError).when_called_with('integer', {'haslo': 'haslo'})

    def test_edycja_haslo_zly_typ_2(self):
        assert_that(self.app.edycja_haslo).raises(
            TypeError).when_called_with(2, 'object')


    def test_edycja_haslo_brak_Wartosci(self):
        assert_that(self.app.edycja_haslo).raises(
            ValueError).when_called_with('')

    @patch('src.application.requests.put')
    def test_edycja_haslo_inne_bledy(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        response = self.app.edycja_haslo('haslo')
        assert_that(response).is_equal_to_ignoring_case('Ups... Coś poszło nie tak')

    @patch('src.application.requests.put')
    def test_edycja_haslo_inne_bledy_mock(self, mock_put):
        create_request_mock(mock_put, FakeResponse(403))
        self.app.edycja_haslo('haslo')
        mock_put.assert_called_once()

    def test_edycja_hasla_haslo_puste(self):
        assert_that(self.app.edycja_haslo).raises(
            ValueError).when_called_with('')

    def test_edycja_hasla_haslo_int(self):
        assert_that(self.app.edycja_haslo).raises(
            ValueError).when_called_with(1)


    def test_edycja_hasla_haslo_float(self):
        assert_that(self.app.edycja_haslo).raises(
            ValueError).when_called_with(1.7)





