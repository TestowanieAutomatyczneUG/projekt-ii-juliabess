import requests


class ZalogujSie:


    def __init__(self):

        self.add = "https://kocham.testowanie/add"
        self.update = "https://kocham.testowanie/update"
        self.delete = "https://kocham.testowanie/delete"
        self.register = "https://kocham.testowanie/register"
        self.loginn = "https://kocham.testowanie/login"
        self.get = "https://kocham.testowanie/users"
        self.getOne = "https://kocham.testowanie/{}"

    def rejestracja(self, pesel, login, haslo):
        if type(pesel) is not str:
            raise ValueError
        if len(pesel) != 11:
            raise ValueError
        if type(login) is not str:
            raise ValueError
        if len(login) <= 0:
            raise ValueError
        if type(haslo) is not str:
            raise ValueError
        if len(haslo) <= 0:
            raise ValueError

        body = {'pesel': pesel, 'login': login, 'haslo':haslo}
        response = requests.post(self.register , json=body)
        if 200 <= response.status_code <= 299:
            return response
        elif response.status_code == 409:
            return 'Podany użytkownik już istnieje'
        else:
            return 'Ups... Coś poszło nie tak'


    def login(self, login, haslo):
        if type(login) is not str:
            raise ValueError
        if len(login) < 1:
            raise ValueError
        if type(haslo) is not str:
            raise ValueError
        if len(haslo) < 1:
            raise ValueError

        body = {'login': login, 'haslo':haslo}
        response = requests.post(self.login , json=body)
        if 200 <= response.status_code <= 299:
            return response
        elif response.status_code == 409:
            return 'Podany login lub hasło jest nieprawidłowy'
        else:
            return 'Ups... Coś poszło nie tak'

    def usun(self, login):
        if type(login) is not str:
            raise ValueError
        if len(login) < 1:
            raise ValueError


        body = {'login': login}
        response = requests.delete(self.delete, json=body)
        if 200 <= response.status_code <= 299:
            return response
        else:
            return 'Ups... Coś poszło nie tak'