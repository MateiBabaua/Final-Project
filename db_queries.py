import sqlite3

# /*--------------------------------------------------------------
# Fisier destinat pentru sql queies
# --------------------------------------------------------------*/

database_name = 'database.db'
def create_frameworks_table(database_name, frameworks):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

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


def create_social_links(database_name, table_name, data):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (website TEXT, link TEXT)')
    cursor.executemany(f"INSERT INTO {table_name} (website, link) VALUES (?, ?)", data)

    conn.commit()
    conn.close()


def create_project_link(database_name, project_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Repositories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repository TEXT NOT NULL,
            link TEXT NOT NULL
        );
    ''')

    cursor.executemany('''
        INSERT INTO Repositories (repository, link)
        VALUES (?, ?)
    ''', project_name)

    conn.commit()
    conn.close()


frameworks = ["Django", "Flask", "Bootstrap", "Sass/Scss"]
create_frameworks_table(database_name, frameworks)

website_data = [
    ('Facebook', 'https://www.facebook.com/matei.babb'),
    ('Instagram', 'https://www.instagram.com/mateibab_/'),
    ('GitHub', 'https://github.com/MateiBabaua'),
    ('LinkedIn', 'https://www.linkedin.com/in/mateibabaua/')]
create_social_links('database.db', 'Websites', website_data)

project_names = [
    ('scraping', 'https://github.com/peviitor-ro/Scrapers_Matei'),
    ('electronical catalogue', 'https://github.com/MateiBabaua/ElectronicalCatalogue'),
    ('personal', 'https://mateibabaua.github.io/')]
create_project_link(database_name, project_names)
