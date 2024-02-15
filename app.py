from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.config['DATABASE'] = 'database.db'


# /*--------------------------------------------------------------------------------------
#                                          Home Page
# --------------------------------------------------------------------------------------*/


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


class ContactInfo:     # About -> Contact
    def __init__(self, database):
        self.database = database

    def get_info(self):
        query_result = self.database.execute_query("SELECT * FROM Contacte")
        return query_result[0] if query_result else None


class Technologies:     #About -> Technologies
    def __init__(self, database):
        self.database = database

    def get_technologies(self):
        query_result = self.database.execute_query("SELECT Technology FROM Technologies")
        return [row[0] for row in query_result]


class Frameworks:     #About -> Frameworks
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


def create_messages_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()


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
    create_messages_table()

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


@app.route('/blog')
def blog():
    database = Database('database.db')

    get_contact_info = ContactInfo(database).get_info()

    return render_template('blog.html',
                           contact_info=get_contact_info,)


if __name__ == '__main__':
    app.run(debug=True)
