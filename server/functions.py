import aiosqlite

DATABASE = "data.db"

async def save_game_data(token: str, board: str, game_name: str, player_1: str, turn: str) -> None:
    """
    Сохраняет данные шахматной партии в базу данных.
    """
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT INTO games (game_token, board, game_name, player_1, player_2, turn) VALUES (?, ?, ?, ?, ?, ?)",
            (token, board, game_name, player_1, None, turn)
        )
        await db.commit()


async def edit_board(token: str, board_list: str) -> None:
    """
    Сохраняет данные шахматной партии в базу данных.
    """
    # Преобразуем список обратно в строку
    board_str = str(board_list)

    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "UPDATE games SET board = ? WHERE game_token = ?",
            (board_str, token)
        )
        await db.commit()

async def get_all_game_tokens() -> list:
    """
    Возвращает список всех токенов игр из базы данных.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT game_token FROM games WHERE status IN (0, 1)") as cursor:
            rows = await cursor.fetchall()
            tokens = [row[0] for row in rows]  # Извлекаем токены из строк
    return tokens

async def edit_status_by_token(token: str):
    """
    Возвращает токен игры по её названию.
    """
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "UPDATE games SET status = status + 1 WHERE game_token = ?",
            (token,)
        )
        await db.commit()

async def get_game_names() -> list:
    """
    Возвращает список всех игр из базы данных.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT game_name FROM games WHERE status IN (0, 1)") as cursor:
            rows = await cursor.fetchall()
            names = [row[0] for row in rows]  # Извлекаем токены из строк
    return names

async def get_board_by_token(token: str) -> str:
    """
    Возвращает состояние доски по токену игры из базы данных.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT board FROM games WHERE game_token = ?", (token,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем состояние доски
            else:
                return None


async def get_status(token: str) -> str:
    """
    Возвращает статус игры по её токену.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT status FROM games WHERE game_token = ?", (token,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем статус игры
            else:
                return None


async def get_player_1_by_token(token: str) -> str:
    """
    Возвращает токен игры по её названию.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT player_1 FROM games WHERE game_token = ?", (token,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем первого игрока
            else:
                return None


async def edit_player_2_by_token(token: str, player_2: str):
    """
    Изменяет статус игры по её токену.
    """
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "UPDATE games SET player_2 = ? WHERE game_token = ?",
            (player_2, token)
        )
        await db.commit()


async def get_token_st() -> list:
    """
    Возвращает список всех токенов игр из базы данных.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT game_token FROM games WHERE status IN (0, 1)") as cursor:
            rows = await cursor.fetchall()
            tokens = [row[0] for row in rows]  # Извлекаем токены из строк
    return tokens


async def get_turn_by_token(token: str) -> str:
    """
    Возвращает токен игры по её названию.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT turn FROM games WHERE game_token = ?", (token, )) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем ход игры
            else:
                return None


async def edit_turn_by_token(token: str, turn: str):
    """
    Изменяет статус игры по её токену.
    """
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "UPDATE games SET turn = ? WHERE game_token = ?",
            (turn, token)
        )
        await db.commit()


async def get_player_2_by_token(token: str) -> str:
    """
    Возвращает токен игры по её названию.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT player_2 FROM games WHERE game_token = ?", (token, )) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]  # Возвращаем второго игрока
            else:
                return None