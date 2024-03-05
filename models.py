import sqlite3
from datetime import datetime


class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


def create_connection(database_name):
    conn = sqlite3.connect(database_name)
    return conn

# /*--------------------------------------------------------------------------------------
#                                          Home Page
# --------------------------------------------------------------------------------------*/


class ContactInfo:
    def __init__(self, database):
        self._database = database

    def get_info(self):
        query_result = self._database.execute_query("SELECT * FROM Contacte")
        return query_result[0] if query_result else None


class Technologies:
    def __init__(self, database):
        self._database = database

    def get_technologies(self):
        query_result = self._database.execute_query("SELECT Technology FROM Technologies")
        return [row[0] for row in query_result]


class Frameworks:
    def __init__(self, database):
        self._database = database

    def get_frameworks(self):
        query_result = self._database.execute_query("SELECT Framework FROM Frameworks")
        return [row for row in query_result]


class Websites:     # Contact -> Icons
    def __init__(self, database):
        self._database = database

    def get_website(self):
        query = "SELECT website, link FROM websites"
        return self._database.execute_query(query)


class ProjectLinks:     # Projects -> GitHub Links
    def __init__(self, database):
        self._database = database

    def get_github_links(self):
        query = "SELECT link FROM Repositories"
        return self._database.execute_query(query)


# /*--------------------------------------------------------------------------------------
#                                          Blog Page
# --------------------------------------------------------------------------------------*/

class Comments:
    def __init__(self, name, reply, date):
        self.name = name
        self.reply = reply
        self.date = date


class BlogComments:
    def __init__(self, database):
        self.database = database

    def get_comments(self):
        query = "SELECT name, reply, strftime('%d-%m-%Y %H:%M:%S', date) AS date FROM Replies"

        try:
            rows = self.database.execute_query(query)
            comments = [Comments(name, reply, date) for name, reply, date in rows]
            return comments
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def add_comment(self, name, email, reply):
        formatted_date = datetime.now().strftime('%d-%m-%Y')
        try:
            conn = create_connection('database.db')
            cursor = conn.cursor()
            query = cursor.execute('''
                INSERT INTO Replies (name, email, reply, date) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (name, email, reply))
            self.database.execute_query(query, (name, email, reply, formatted_date))
            conn.commit()
        except sqlite3.Error as e:
            print("Error inserting data:", e)
            raise
        finally:
            conn.close()

    @staticmethod
    def count_rows():
        conn = create_connection('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Replies")
        total_rows = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        return total_rows
