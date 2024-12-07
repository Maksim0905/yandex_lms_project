import requests
import os
import urllib.parse
from config import default_server

# URL API
create_game_url = f"http://{default_server}/create_game/"
get_all_tokens_url = f"http://{default_server}/get_all_tokens/"
get_board_url = f"http://{default_server}/get_board/"
edit_board_url = f"http://{default_server}/edit_board/"
get_all_names_url = f"http://{default_server}/get_game_names/"
edit_status_url = f"http://{default_server}/edit_status_by_token/"
get_status_url = f"http://{default_server}/get_status_by_token/"
get_player_1_url = f"http://{default_server}/get_player_1_by_token/"
get_player_2_url = f"http://{default_server}/edit_player_2_by_token/"
get_turn_by_token_url = f"http://{default_server}/get_turn_by_token/"
edit_turn_by_token_url = f"http://{default_server}/edit_turn/"
get_player_2_by_token_url = f"http://{default_server}/get_player_2_by_token/"


def load_username():
    """Загружает имя пользователя из файла, если оно существует."""
    if os.path.exists("username.txt"):
        with open("username.txt", "r") as file:
            return file.read().strip()
    else:
        return None


def create_game(game_name: str, turn: str):
    """
    Создает новую шахматную игру через API и возвращает токен игры.
    """
    # Загружаем имя игрока из файла
    player_1 = load_username()
    
    if not player_1:
        print("Ошибка: Имя игрока не найдено в файле username.txt.")
        return None
    
    # Данные для запроса
    data = {
        "game_name": game_name,  # Имя игры
        "player_1": player_1,    # Имя первого игрока
        "turn": turn             # Чей ход
    }

    # Заголовки для указания типа содержимого
    headers = {
        "Content-Type": "application/json"
    }

    # Выполнение POST-запроса для создания игры
    response = requests.post(create_game_url, json=data, headers=headers)

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        token = response.json().get("token")
        if token:
            print(f"Игра '{game_name}' успешно создана. Токен: {token}")
            return token
        else:
            print("Ошибка: Токен игры не получен.")
            return None
    else:
        print(f"Ошибка при создании игры. Статус: {response.status_code}")
        print(f"Ответ от сервера: {response.text}")
        return None
    

def get_all_game_tokens():
    """
    Выполняет запрос к API для получения списка всех токенов игр.
    """
    # Выполнение GET-запроса
    response = requests.get(get_all_tokens_url)

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        tokens = response.json().get("tokens", [])
        return tokens
    else:
        return None

def get_board_by_token(token):
    """
    Выполняет запрос к API для получения состояния доски по токену игры.
    """
    # Выполнение GET-запроса для получения доски по токену
    response = requests.get(get_board_url, params={"token": token})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        board = response.json()
        # print(response.text)
        return board
    else:
        return None


def edit_board_by_token(token, board):
    """Редактирует состояние доски по токену игры."""
    headers = {"Content-Type": "application/json"}
    # Send the board directly as the request body, without wrapping it in a dictionary
    response = requests.post(
        f"{edit_board_url}?token={token}",
        json=board,  # Send board directly, not {"board": board}
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка: {response.status_code}, Ответ: {response.text}")
        return None

    

def get_names():
    """
    Выполняет запрос к API для получения списка всех игр.
    """
    # Выполнение GET-запроса для получения списка всех игр
    response = requests.get(get_all_names_url)

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        names = response.json()
        return names
    else:
        return None
    

def get_token_by_game_name(game_name: str):
    """
    Возвращает токен игры по её названию.
    """
    tokens = get_all_game_tokens()
    names = get_names()
    if tokens is None or names is None:
        return None
    for i in range(len(names)):
        if names[i] == game_name:
            return tokens[i]
    return None


def edit_status_by_token(token):
    """
    Выполняет запрос к API для редактирования статуса игры по токену.
    """
    # Выполнение POST-запроса для редактирования статуса игры по токену
    response = requests.post(edit_status_url, params={"token": token})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def get_status(token):
    """
    Выполняет запрос к API для получения статуса игры по токену.
    """
    # Выполнение GET-запроса для получения статуса игры по токену
    response = requests.get(get_status_url, params={"token": token})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        status = response.json()
        return status
    else:
        return None


def get_player_1_by_token(token):
    """
    Выполняет запрос к API для получения имени первого игрока по токену игры.
    """
    # Выполняет запрос к API для получения имени первого игрока по токену игры
    response = requests.get(get_player_1_url, params={"token": token})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        player_1 = response.json()
        return player_1
    else:
        return None
    

def get_player_2_by_token(token):
    """
    Выполняет запрос к API для получения имени второго игрока по токену игры.
    """
    # Выполняет запрос к API для получения имени второго игрока по токену игры
    response = requests.post(get_player_2_by_token_url, params={"token": token})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        player_2 = response.json()
        return player_2
    else:
        return None


def edit_player_2_by_token(token, player_2):
    """
    Выполняет запрос к API для редактирования имени второго игрока по токену игры.
    """
    # Выполняет запрос к API для редактирования имени второго игрока по токену игры
    response = requests.post(get_player_2_url, params={"token": token, "player_2": player_2})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def get_turn_by_token(token):
    """
    Выполняет запрос к API для получения хода по токену игры.
    """
    # Выполняет запрос к API для получения хода по токену игры
    response = requests.get(get_turn_by_token_url, params={"token": token})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        turn = response.json()
        return turn
    else:
        return None
    
    # if response.status_code == 200:
    #     turn = response.text.strip('"')
    #     return turn
    # else:
    #     return None
    

def edit_turn_by_token(token, turn):
    """
    Выполняет запрос к API для редактирования хода по токену игры.
    """
    # Выполняет запрос к API для редактирования хода по токену игры
    response = requests.post(edit_turn_by_token_url, params={"token": token, "turn": turn})

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def load_username():
        """Загружает имя пользователя из файла"""
        if os.path.exists("username.txt"):
            with open("username.txt", "r") as file:
                return file.read().strip()
        else:
            return None