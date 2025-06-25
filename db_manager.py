# db_manager.py
import mysql.connector
from config import DB_CONFIG
""" Codigo copiado de motores externos e IA"""
class DatabaseManager:
    """
    Gestiona la conexión y desconexión a la base de datos MySQL.
    """
    def __init__(self, db_config):
        """
        Inicializa  la configuración de la Base de Datos.
        """
        self.db_config = db_config
        self._connection = None

    def get_connection(self):
        """
        Establece y devuelve una conexión a la base de datos.
        Si la conexión ya existe y está activa, la devuelve.
        """
        if self._connection and self._connection.is_connected():
            return self._connection
        try:
            self._connection = mysql.connector.connect(**self.db_config)
            return self._connection
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            self._connection = None  # Asegurarse de que no queda una conexión rota
            return None

    def close_connection(self):
        """
        Cierra la conexión a la base de datos si está abierta.
        """
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None
            # print("Conexión a la base de datos cerrada.")

    def get_cursor(self, dictionary=False):
        """
        Obtiene un cursor de la conexión actual.
        """
        conn = self.get_connection()
        if conn:
            return conn.cursor(dictionary=dictionary)
        return None

    def commit(self):
        """
        Confirma los cambios pendientes en la base de datos.
        """
        conn = self.get_connection()
        if conn:
            conn.commit()

    def rollback(self):
        """
        Revierte los cambios pendientes en la base de datos.
        """
        conn = self.get_connection()
        if conn:
            conn.rollback()
