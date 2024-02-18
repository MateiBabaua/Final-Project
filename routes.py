from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import (Database,
                    ContactInfo,
                    Technologies,
                    Frameworks,
                    Websites,
                    ProjectLinks,
                    BlogComments)


app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.config['DATABASE'] = 'database.db'


def create_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn

# /*--------------------------------------------------------------------------------------
#                                          Home Page
# --------------------------------------------------------------------------------------*/


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

# /*--------------------------------------------------------------------------------------
#                                          Blog Page
# --------------------------------------------------------------------------------------*/


@app.route('/blog')
def blog():
    database = Database('database.db')

    get_db_contact_info = ContactInfo(database).get_info()
    get_db_blog_comments = BlogComments(database).get_comments()
    get_db_comments_count = BlogComments(database).count_rows()
    get_db_websites_links = Websites(database).get_website()

    return render_template('blog.html',
                           contact_info=get_db_contact_info,
                           comments=get_db_blog_comments,
                           comments_index=get_db_comments_count,
                           websites=get_db_websites_links,)


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
