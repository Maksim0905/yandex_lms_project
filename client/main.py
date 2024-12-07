from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtCore import QTimer  # Импортируем QTimer для создания таймера
import sys
import os
import api  # Ваш модуль API
from chess import ChessBoard

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('main.ui', self)

        self.games = []  # Игры будут загружаться через API
        self.token = None
        # Заполнение QComboBox
        self.populate_games()

        # Подключение сигналов и слотов
        self.pushButton.clicked.connect(self.play_game)
        self.pushButton_2.clicked.connect(self.refresh_games)
        self.pushButton_3.clicked.connect(self.create_game)

        self.update_lcd()

        # Инициализация имени пользователя
        self.username = self.load_username()
        self.display_username()

        # Настроим таймер, который будет обновлять игры каждые 5 секунд
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_games)  # Привязываем к методу refresh_games
        self.timer.start(10000)  # Запуск таймера с интервалом 5000 мс (5 секунд)

    def populate_games(self):
        """Заполняет QComboBox списком игр, полученных с API."""
        self.comboBox.clear()
        
        # Получаем список игр через API
        games_from_api = api.get_names()  # Получаем все игры через API
        
        if games_from_api:
            if games_from_api:  # Если игры получены
                self.games = games_from_api  # Сохраняем список игр
                self.comboBox.addItems(self.games)  # Добавляем игры в ComboBox
            else:
                # Предлагаем пользователю создать игру
                self.create_game()
        else:
            pass


    def update_lcd(self):
        """Обновляет QLCDNumber количеством игр."""
        count = len(self.games)
        self.lcdNumber.display(count)

    def play_game(self):
        """Действие при нажатии кнопки '▶ Играть'."""
        selected_game = self.comboBox.currentText()
        if selected_game:
            token = api.get_token_by_game_name(selected_game)
            status = api.get_status(token)
            if status == '0':
                game = ChessBoard(token=token, player_1=self.username, player_2=None, turn=self.username, title_name = selected_game)
                game.start_background_update()
                game.setParent(self)
                chessboard_width = game.width()
                chessboard_height = game.height()

                # Изменяем размер главного окна в зависимости от размеров шахматной доски
                self.resize(chessboard_width, chessboard_height)
                self.setWindowTitle(selected_game)
                self.update()
                game.show()
                api.edit_status_by_token(token)
            elif status == '1':
                player_1 = api.get_player_1_by_token(token)
                api.edit_player_2_by_token(token, self.username)
                game = ChessBoard(token=token, player_1=player_1, player_2=self.username, turn=player_1, title_name = selected_game)
                game.start_background_update()
                game.setParent(self)
                chessboard_width = game.width()
                chessboard_height = game.height()

                # Изменяем размер главного окна в зависимости от размеров шахматной доски
                self.resize(chessboard_width, chessboard_height)
                self.setWindowTitle(selected_game)
                self.update()
                game.show()
                api.edit_status_by_token(token)
            
            elif status == '2':
                QMessageBox.warning(self, "Предупреждение", "Игра заполнена!")


            # QMessageBox.information(self, "Играть", f"Запуск игры: {selected_game}")
        else:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите игру.")

    def refresh_games(self):
        """Действие при нажатии кнопки '🔄' или таймере."""
        # Перезагружаем игры с API
        self.populate_games()
        self.update_lcd()

    def create_game(self):
        """Действие при нажатии кнопки '✏️ Создать игру'."""
        # Запрашиваем у пользователя название игры
        text, ok = QInputDialog.getText(self, "Создать новую игру", "Введите название игры:")
        if ok and text:
            # Загружаем имя игрока из файла
            player_1 = api.load_username()
            
            if not player_1:
                QMessageBox.warning(self, "Ошибка", "Не удалось найти имя пользователя в файле username.txt.")
                return
            
            # Создаем игру через API
            new_game_data = api.create_game(game_name=text, turn=player_1)  # Указываем имя игры и чей ход
            if new_game_data:
                # Если игра успешно создана, обновляем список игр
                self.populate_games()
                self.update_lcd()
                QMessageBox.information(self, "Создание игры", f"Игра '{text}' успешно добавлена!")

            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось создать игру.")


    def load_username(self):
        """Загружает имя пользователя из файла, если оно существует."""
        if os.path.exists("username.txt"):
            with open("username.txt", "r") as file:
                return file.read().strip()
        else:
            return None

    def save_username(self, username):
        """Сохраняет имя пользователя в файл."""
        with open("username.txt", "w") as file:
            file.write(username)

    def display_username(self):
        """Отображает имя пользователя в правом верхнем углу."""
        if self.username:
            self.label.setText(f"Привет, {self.username}!")
        else:
            self.ask_for_username()

    def ask_for_username(self):
        """Запрашивает имя пользователя при первом запуске программы."""
        text, ok = QInputDialog.getText(self, "Введите имя", "Введите ваше имя:")
        if ok and text:
            self.username = text
            self.save_username(text)
            self.display_username()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle("Игровые Комнаты")
    window.show()
    sys.exit(app.exec())
