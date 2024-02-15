import sqlite3
# /*--------------------------------------------------------------------------------------
#                                          Database Queries
# --------------------------------------------------------------------------------------*/
database = 'database.db'

# /*--------------------------------------------------------------------------------------
#                                          Contact
# --------------------------------------------------------------------------------------*/


def create_contact_table(database_name, name, profile, email, phone):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Contacte'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''CREATE TABLE IF NOT EXISTS Contacte (
                            ID INTEGER PRIMARY KEY,
                            Name TEXT,
                            Profile TEXT,
                            Email TEXT,
                            Phone TEXT
                        )''')

        cursor.execute('''INSERT INTO Contacte (Name, Profile, Email, Phone)
                              VALUES (?, ?, ?, ?)''', (name, profile, email, phone))

        conn.commit()
        conn.close()
    else:
        conn.commit()
        conn.close()


nume = 'Babaua Matei-Paul'
profil = 'Junior Python Developer & Junior Automation Tester'
email = 'mateibabaua@gmail.com'
telefon = '+40 (765) 303 172'
create_contact_table(database, nume, profil, email, telefon)

# /*--------------------------------------------------------------------------------------
#                                          Technologies
# --------------------------------------------------------------------------------------*/


def create_technologies_table(database_name, technologies):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Technologies'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''CREATE TABLE IF NOT EXISTS Technologies (
                            ID INTEGER PRIMARY KEY,
                            Technology TEXT,
                            Competence_Level TEXT
                        )''')

        for tech, competence_level in technologies.items():
            cursor.execute('''INSERT INTO Technologies (Technologies, Competence_Level)
                                  VALUES (?, ?)''', (tech, "Nivel prestabilit"))

        conn.commit()
        conn.close()
    else:
        conn.commit()
        conn.close()


technologies = ["Python", "C++", "HTML5", "CSS3", "JavaScript", "MySQL", "SQLite", "MongoDB", "SQLAlchemy"]
create_technologies_table(database, technologies)

# /*--------------------------------------------------------------------------------------
#                                          Frameworks
# --------------------------------------------------------------------------------------*/


def create_frameworks_table(database_name, frameworks):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Frameworks'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''CREATE TABLE IF NOT EXISTS Frameworks (
                            ID INTEGER PRIMARY KEY,
                            Framework TEXT,
                            Competence_Level TEXT
                        )''')

        for framework in frameworks:
            cursor.execute('''INSERT INTO Frameworks (Framework, Competence_Level)
                              VALUES (?, ?)''', (framework, "Nivel prestabilit"))

        conn.commit()
        conn.close()
    else:
        conn.commit()
        conn.close()


frameworks = ["Django", "Flask", "Bootstrap", "SaSS/ScSS"]
create_frameworks_table(database, frameworks)

# /*--------------------------------------------------------------------------------------
#                                          Socials
# --------------------------------------------------------------------------------------*/


def create_social_links_table(database_name, data):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Websites'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''CREATE TABLE IF NOT EXISTS Websites (
                       website TEXT,
                       link TEXT
                       )''')
        cursor.executemany('''INSERT INTO Websites (website, link) 
                                VALUES (?, ?)''', data)

        conn.commit()
        conn.close()
    else:
        conn.commit()
        conn.close()


website_data = [
    ('Facebook', 'https://www.facebook.com/matei.babb'),
    ('Instagram', 'https://www.instagram.com/mateibab_/'),
    ('GitHub', 'https://github.com/MateiBabaua'),
    ('LinkedIn', 'https://www.linkedin.com/in/mateibabaua/')]
create_social_links_table(database, website_data)

# /*--------------------------------------------------------------------------------------
#                                          GitHub Links
# --------------------------------------------------------------------------------------*/


def create_project_link_table(database_name, project_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Repositories'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repository TEXT NOT NULL,
                link TEXT NOT NULL
            );''')

        cursor.executemany('''
            INSERT INTO Repositories (repository, link)
            VALUES (?, ?)
        ''', project_name)

        conn.commit()
        conn.close()
    else:
        conn.commit()
        conn.close()


project_names = [
    ('scraping', 'https://github.com/peviitor-ro/Scrapers_Matei'),
    ('electronical catalogue', 'https://github.com/MateiBabaua/ElectronicalCatalogue'),
    ('personal', 'https://mateibabaua.github.io/')]
create_project_link_table(database, project_names)

# /*--------------------------------------------------------------------------------------
#                                          Message Table
# --------------------------------------------------------------------------------------*/


def create_messages_table(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Messages'")
    table_exists = cursor.fetchone()

    if not table_exists:
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Messages (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            subject TEXT,
            message TEXT
        )'''

        cursor.execute(create_table_query)

        conn.commit()
        conn.close()
    else:
        conn.commit()
        conn.close()


create_messages_table(database)
