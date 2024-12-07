from fastapi import FastAPI, HTTPException, Body, Query
from functions import (save_game_data, get_all_game_tokens, get_board_by_token, get_game_names,
                       edit_status_by_token, get_status, get_player_1_by_token, edit_player_2_by_token, edit_board,
                       get_turn_by_token, edit_turn_by_token, get_player_2_by_token)
import random
import string
from typing import List
import ast

import aiosqlite

app = FastAPI()


def generate_token(length=16):
    """
    Генерирует токен случайной строки из букв и цифр.
    """
    characters = string.ascii_letters + string.digits  # Включаем буквы (верхнего и нижнего регистра) и цифры
    return ''.join(random.choice(characters) for _ in range(length))


def generate_initial_board():
    """
    Генерирует начальное состояние шахматной доски.
    """
    return [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["wP"] * 8,
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]


@app.post("/create_game/")
async def chess_game(
    game_name: str = Body(...),  # Данные приходят в теле запроса (Body)
    player_1: str = Body(...),   # Данные приходят в теле запроса (Body)
    turn: str = Body(...),       # Данные приходят в теле запроса (Body)
):
    """
    Обрабатывает данные шахматной партии и сохраняет их в базу данных.
    """
    if not game_name or not player_1 or not turn:
        raise HTTPException(status_code=400, detail="Все поля должны быть заполнены.")

    # Генерация случайного токена и начальной доски
    token = generate_token()
    board = generate_initial_board()

    # Преобразование board в строку для сохранения в БД
    board_str = str(board)

    # Сохранение данных в базе
    await save_game_data(token, board_str, game_name, player_1, turn)

    return {"token": token}



@app.get("/get_all_tokens/")
async def get_all_tokens():
    """
    Возвращает список всех токенов игр из базы данных.
    """
    tokens = await get_all_game_tokens()
    return {"tokens": tokens}


@app.get("/get_board/")
async def get_board(token: str):
    """
    Возвращает состояние доски по токену игры.
    """
    board_str = await get_board_by_token(token)
    board = ast.literal_eval(board_str)  # Преобразование строки в список
    return board

@app.post("/edit_board/")
async def edit_game_board(
    token: str = Query(...),  # Параметр token передается через URL
    board: List[List[str]] = Body(...)  # Параметр board передается как JSON
):
    """
    Обрабатывает данные шахматной партии и сохраняет их в базу данных.
    """
    print(board)
    # Преобразуем доску в строку для сохранения в БД (если нужно)
    board_str = str(board)

    # Сохраняем данные в базе данных
    await edit_board(token, board_str)

@app.get("/get_game_names/")
async def game_names():
    """
    Возвращает список всех игр из базы данных.
    """
    names = await get_game_names()
    return names


@app.get("/get_token_by_game_name/")
async def get_token_by_game_name(game_name: str):
    """
    Возвращает токен игры по её названию.
    """
    tokens = await get_all_game_tokens()
    names = await get_game_names()
    for i in range(len(names)):
        if names[i] == game_name:
            return tokens[i]
    return None

@app.post("/edit_status_by_token/")
async def edit_status(token: str):
    """
    Изменяет статус игры по её токену.
    """
    await edit_status_by_token(token)


@app.get("/get_status_by_token")

async def get_game_status(token: str):
    """
    Возвращает статус игры по её токену.
    """
    status = await get_status(token)
    return status


@app.get("/get_player_1_by_token/")
async def player_1_by_token(token: str):
    """
    Возвращает токен игры по её названию.
    """
    player_1 = await get_player_1_by_token(token)

    return player_1


@app.post("/edit_player_2_by_token/")
async def player_2_by_token(token: str, player_2: str):
    """
    Изменяет статус игры по её токену.
    """
    await edit_player_2_by_token(token, player_2)


@app.post("/get_player_2_by_token/")
async def player_2_by_token(token: str):
    """
    Изменяет статус игры по её токену.
    """
    player_2 = await get_player_2_by_token(token)

    return player_2


@app.get("/get_turn_by_token/")
async def get_turn(token: str):
    """
    Возвращает токен игры по её названию.
    """
    turn = await get_turn_by_token(token)

    return turn


@app.post("/edit_turn/")
async def edit_turn(token: str, turn: str):
    """
    Изменяет статус игры по её токену.
    """
    await edit_turn_by_token(token, turn)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=80)