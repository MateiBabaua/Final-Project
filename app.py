from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.config['DATABASE'] = 'database.db'


def create_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn


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


# /*--------------------------------------------------------------------------------------
#                                          Home Page
# --------------------------------------------------------------------------------------*/


class ContactInfo:     # About -> Contact
    def __init__(self, database):
        self.database = database

    def get_info(self):
        query_result = self.database.execute_query("SELECT * FROM Contacte")
        return query_result[0] if query_result else None


class Technologies:
    def __init__(self, database):
        self.database = database

    def get_technologies(self):
        query_result = self.database.execute_query("SELECT Technology FROM Technologies")
        return [row[0] for row in query_result]


class Frameworks:
    def __init__(self, database):
        self.database = database

    def get_frameworks(self):
        query_result = self.database.execute_query("SELECT Framework FROM Frameworks")
        return [row for row in query_result]


class Websites:     # Contact -> Icons
    def __init__(self, database):
        self.database = database

    def get_website(self):
        query = "SELECT website, link FROM websites"
        return self.database.execute_query(query)


class ProjectLinks:     # Projects -> GitHub Links
    def __init__(self, database):
        self.database = database

    def get_github_links(self):
        query = "SELECT link FROM Repositories"
        return self.database.execute_query(query)


@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not subject or not message:
            return 'All fields are required', 400

        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Messages (name, email, subject, message) 
                VALUES (?, ?, ?, ?)
            ''', (name, email, subject, message))
            conn.commit()
        except sqlite3.Error as e:
            print("Error inserting data:", e)
            return 'An error occurred while saving your message', 500
        finally:
            conn.close()

        return redirect(url_for('index'))


@app.route('/')
def index():
    database = Database('database.db')

    get_db_contact_info = ContactInfo(database).get_info()
    get_db_technologies_data = Technologies(database).get_technologies()
    get_db_frameworks_data = Frameworks(database).get_frameworks()
    get_db_websites_links = Websites(database).get_website()
    get_db_project_links = ProjectLinks(database).get_github_links()

    return render_template(
        'index.html',
        contact_info=get_db_contact_info,
        technologies=get_db_technologies_data,
        frameworks=get_db_frameworks_data,
        websites=get_db_websites_links,
        project_github_links=get_db_project_links,)


# /*--------------------------------------------------------------------------------------
#                                          Blog Page
# --------------------------------------------------------------------------------------*/

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
            conn = create_connection()
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
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Replies")
        total_rows = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        return total_rows


class Comments:
    def __init__(self, name, reply, date):
        self.name = name
        self.reply = reply
        self.date = date


@app.route('/blogreply', methods=['POST'])
def blogreply():
    if request.method == 'POST':
        name = request.form.get('blogname')
        email = request.form.get('blogemail')
        reply = request.form.get('blogreply')

        if not name or not email or not reply:
            return 'All fields are required', 400

        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Replies (name, email, reply) 
                VALUES (?, ?, ?)
            ''', (name, email, reply))
            conn.commit()
        except sqlite3.Error as e:
            print("Error inserting data:", e)
            return 'An error occurred while saving your message', 500
        finally:
            conn.close()

        return redirect(url_for('blog'))


@app.route('/blog')
def blog():
    database = Database('database.db')

    get_contact_info = ContactInfo(database).get_info()
    get_blog_comments = BlogComments(database).get_comments()
    get_comments_count = BlogComments(database).count_rows()

    return render_template('blog.html',
                           contact_info=get_contact_info,
                           comments=get_blog_comments,
                           comments_index=get_comments_count,)


if __name__ == '__main__':
    app.run(debug=True)
