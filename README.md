# ♟️ Онлайн Шахматы

![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FMaksim0905%2Fyandex_lms_project&count_bg=%2379C83D&title_bg=%23555555&icon=github.svg&icon_color=%23FFFFFF&title=посетителей&edge_flat=false)

## О проекте

Привет! Меня зовут [Maksim0905](https://github.com/Maksim0905), и я рад представить вам мой проект **Онлайн Шахматы**. Это приложение представляет собой шахматный онлайн-клиент, который позволяет пользователям играть в шахматы через интернет в реальном времени. Проект разработан с использованием **FastAPI** для серверной части, **PyQt6** для пользовательского интерфейса и других библиотек для обеспечения функциональности.

Целью проекта является предоставление удобного и функционального инструмента для игры в шахматы онлайн, с возможностью регистрации пользователей, проведения матчей с другими игроками и управления игровым процессом.

### 🌟 Особенности

- **Регистрация пользователей:**
  - Создавайте аккаунт и входите в систему для сохранения прогресса игры и личных данных.
  
- **Онлайн-игры с другими пользователями:**
  - Подключайтесь и играйте с соперниками через интернет. Взаимодействие с сервером для обмена ходами и статусами игры.
  
- **Игровая доска:**
  - Удобный интерфейс для отображения шахматной доски с возможностью перемещения фигур и отображения текущего состояния игры.
  
- **Проверка ходов и правил игры:**
  - Встроенная логика для проверки правильности ходов и соблюдения шахматных правил (например, рокировка, шах и мат и т.д.).
  
- **Асинхронная база данных на aiosqlite:**
  - Использование асинхронной базы данных на базе aiosqlite для эффективной обработки запросов без блокировки основного потока приложения. Высокая производительность и отзывчивость сервера, даже при большом количестве одновременных пользователей.

### 📸 Скриншоты

![Главная страница](https://github.com/Maksim0905/yandex_lms_project/blob/main/screenshots/homepage.png)
![Игровая доска](https://github.com/Maksim0905/yandex_lms_project/blob/main/screenshots/gameboard.png)

### 🛠 Технологии

- [FastAPI](https://fastapi.tiangolo.com/) – Высокопроизводительный веб-фреймворк для создания API на Python.
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/intro) – Библиотека для создания графических пользовательских интерфейсов.
- [aiosqlite](https://github.com/jreese/aiosqlite) – Асинхронная обёртка для SQLite.
### 📋 Установка северной части

Следуйте этим инструкциям, чтобы установить и запустить проект на вашем локальном компьютере.

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Maksim0905/yandex_lms_project.git
2. **Перейдите в папку server**
   ```bash
   cd server
3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
4. **Запуск сервера FastAPI**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 80 --reload

### 📋 Установка клиентской части

Следуйте этим инструкциям, чтобы установить и запустить проект на вашем локальном компьютере.

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Maksim0905/yandex_lms_project.git
2. **Перейдите в папку client**
   ```bash
   cd client
3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
4. **Запуск сервера FastAPI**
   ```bash
   python main.py


### 📋 Сборка файлов в одно .exe приложение
```bash
pip install --upgrade pyinstaller
pyinstaller --onefile --noconsole --icon=iconc.png main.py



