import sqlite3
from datetime import datetime


class Database():
    def __init__(self, db_file):
        """Инициализация данных"""
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_exist_userx(self, user_id):
        """Проверка юзера на наличие в бд"""
        with self.connection:
            user_status = self.cursor.execute("SELECT * FROM storage_users WHERE user_id = ?", (user_id, )).fetchall()
            return bool(len(user_status))

    def add_userx(self, user_id):
        """Добавление юзера в бд"""
        with self.connection:
            return self.cursor.execute("INSERT INTO storage_users VALUES(?,?)", (user_id, 0))

    def get_thanks_userx(self, user_id):
        """Просмотр количества симпатий у юзера"""
        with self.connection:
            return self.cursor.execute("SELECT thanks_count FROM storage_users WHERE user_id = ?", (user_id, )).fetchone()

    def add_thanks_userx(self, user_id, thanks_count):
        """Добавление симпатии для юзера"""
        with self.connection:
            return self.cursor.execute("UPDATE storage_users SET thanks_count = ? WHERE user_id = ?", (thanks_count, user_id))
        
    def get_banned_userx(self, user_id):
        """Проверка юзера на наличие в базе спаммеров"""
        with self.connection:
            user_status = self.cursor.execute("SELECT * FROM storage_banned WHERE user_id = ?", (user_id, )).fetchall()
            return bool(len(user_status))
    
    def add_banned_userx(self, user_id):
        """Добавление юзера в список спаммеров"""
        with self.connection:
            return self.cursor.execute("INSERT INTO storage_banned VALUES(?)", (user_id, ))
    
    def add_channelx(self, chat_id, channel_url):
        """Добавление канала в базу"""
        with self.connection:
            return self.cursor.execute("INSERT INTO storage_channels VALUES(?, ?)", (chat_id, channel_url))
    
    def get_exist_channelx(self, chat_id):
        """Проверка канала на наличие в бд"""
        with self.connection:
            user_status = self.cursor.execute("SELECT * FROM storage_channels WHERE chat_id= ?", (chat_id, )).fetchall()
            return bool(len(user_status))
    
    def get_channelx(self, chat_id):
        """Просмотр привязанного к чату канала"""
        with self.connection:
            return self.cursor.execute("SELECT channel_url FROM storage_channels WHERE chat_id = ?", (chat_id, )).fetchone()
    
    def delete_channelx(self, chat_id):
        """Удаление чата из бд"""
        with self.connection:
            return self.cursor.execute("DELETE FROM storage_channels WHERE chat_id = ?", (chat_id, ))