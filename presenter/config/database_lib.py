"""Module for interaction with SQLite"""

import sqlite3
from presenter.config.files_paths import DATABASE_FILE
from presenter.config.log import Logger, LOG_TO

LOG = Logger(LOG_TO)


class Database:
    """Управление базой данных"""

    def __init__(self, to_log=True):
        """Подключается к базе данных"""
        if to_log:
            LOG.log("Init database")
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.to_log = to_log

    def __del__(self):
        """Отключается от базы данных"""
        if self.to_log:
            LOG.log("Closing database")
        self.connection.close()  # Закрываем БД

    def get(self, table, *column_value):
        """Read one entry in one table of the database"""
        sql = f"SELECT * FROM {table} WHERE "
        reqs = []
        for value in column_value:
            val = str(value[1]).replace('"', '').replace("'", "")
            reqs.append(f"{value[0]}='{val}'")
        sql += " AND ".join(reqs)
        if self.to_log:
            LOG.log("[SQL]: " + sql)
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            return dict(zip([c[0] for c in self.cursor.description], row))
        return None

    def get_many(self, table, *column_value):
        """Read several entries in one table of the database"""
        sql = f"SELECT * FROM {table} WHERE "
        reqs = []
        for value in column_value:
            val = str(value[1]).replace('"', '').replace("'", "")
            reqs.append(f"{value[0]}='{val}'")
        sql += " AND ".join(reqs)
        if self.to_log:
            LOG.log("[SQL]: " + sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if rows:
            return [dict(zip([c[0] for c in self.cursor.description], row)) for row in rows]
        return []

    def get_all(self, table, order_by='id', how_sort='DESC'):  # how_sort can be equal to ASC
        """Read all entries in one table of the database"""
        sql = "SELECT rowid, * FROM {} ORDER BY {} {}".format(table, order_by, how_sort)
        if self.to_log:
            LOG.log("[SQL]: " + sql)
        all_list = []
        for element in self.cursor.execute(sql):
            all_list.append(dict(zip([c[0] for c in self.cursor.description], element)))
        return all_list

    def change(self, set_what, set_where, table, *column_value):
        """Меняет что-то в базе данных"""
        reqs = []
        for value in column_value:
            val = str(value[1]).replace('"', '').replace("'", "")
            reqs.append(f"{value[0]}='{val}'")
        set_what = str(set_what).replace('"', '').replace("'", "")
        # Одинарные кавычки в sql очень важны
        sql = f"UPDATE {table}\n"
        sql += f"SET {set_where} = '{set_what}'\n"
        sql += "WHERE " + " AND ".join(reqs)
        if self.to_log:
            LOG.log("[SQL]: " + sql)
        self.cursor.execute(sql)
        self.connection.commit()  # Сохраняем изменения

    def increase(self, increase_value, increase_where, table, *column_value):
        """Increase value in table"""
        reqs = []
        for value in column_value:
            val = str(value[1]).replace('"', '').replace("'", "")
            reqs.append(f"{value[0]}='{val}'")
        sql = f"UPDATE {table}\n"
        sql += f"SET {increase_where} = {increase_where}+{increase_value}\n"
        sql += "WHERE " + " AND ".join(reqs)
        if self.to_log:
            LOG.log("[SQL]: " + sql)
        self.cursor.execute(sql)
        self.connection.commit()

    def append(self, values, table):
        """Добавляет запись в базу данных"""
        try:
            sql = """
            INSERT INTO {}
            VALUES {}
            """.format(table, tuple(map(str, values)))
            if self.to_log:
                LOG.log("[SQL]: " + sql)
            self.cursor.execute(sql)
        except sqlite3.OperationalError as exception:
            LOG.log(exception)
        self.connection.commit()  # Сохраняем изменения

    def remove(self, table, *column_value):
        """Remove an entry from a database"""
        sql = f"DELETE FROM {table} WHERE "
        reqs = []
        for value in column_value:
            val = str(value[1]).replace('"', '').replace("'", "")
            reqs.append(f"{value[0]}='{val}'")
        sql += " AND ".join(reqs)
        if self.to_log:
            LOG.log("[SQL]: " + sql)
        self.cursor.execute(sql)
        self.connection.commit()
