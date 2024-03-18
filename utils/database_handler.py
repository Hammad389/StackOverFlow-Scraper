import json
from sqlite3 import connect
import os


class Json_Handler(object):

    # TO SAVE THE QUESTIONS IDS
    def __init__(self,
                 questions_ids_file_path: str = './database/scraped_questions_ids.json',
                 scraped_pages_index_file_path: str = './database/scraped_pages_index.json'
                 ) -> None:
        self.questions_ids_file_path: str = os.path.abspath(questions_ids_file_path)
        self.scraped_question_ids = self.load_scraped_ids()
        self.scraped_pages_index_file_path: str = os.path.abspath(scraped_pages_index_file_path)
        self.scraped_page_index = self.load_scraped_pages_index()

    def load_scraped_ids(self):
        try:
            with open(self.questions_ids_file_path, 'r') as file:
                file_content = file.read()
                if file_content:
                    return set(json.loads(file_content))
                else:
                    return set()
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    def save_scraped_id(self, question_id):
        scraped_ids = self.load_scraped_ids()
        scraped_ids.add(question_id)

        with open(self.questions_ids_file_path, 'w') as file:
            json.dump(list(scraped_ids), file)

    def is_exist(self, question_id):
        return question_id in self.scraped_question_ids

    def add_question_id(self, question_id):
        self.save_scraped_id(question_id)

    # TO SAVE THE PAGE NUMBER
    def load_scraped_pages_index(self):
        try:
            with open(self.scraped_pages_index_file_path, 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_scraped_pages_index(self, page_id):
        with open(self.scraped_pages_index_file_path, 'w') as file:
            file.write(str(page_id))


class Database_Handler(object):

    def __init__(self,
                 database_path: str = './database',
                 database_file_name: str = 'python_question_answers_snippets.db'
                 ) -> None:
        self.database_path: str = os.path.abspath(database_path)
        self.database_file_name: str = database_file_name
        if not os.path.isdir(self.database_path):
            os.mkdir(self.database_path)
        self.create_database()

    def create_connection(self):
        database_file_path = os.path.join(self.database_path, f'{self.database_file_name}')
        database_connection = connect(database_file_path)
        cursor = database_connection.cursor()
        return database_connection, cursor

    def create_database(self) -> None:
        database_connection, cursor = self.create_connection()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS snippets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        code TEXT,
        source TEXT
        )""")

    def insert_into_database(self, title, code, source) -> bool:
        database_connection, cursor = self.create_connection()

        try:
            cursor.execute("""INSERT INTO snippets(title, code, source) VALUES (?, ?, ?)""",
                           (title, code, source))

            # Commit the changes to the database before closing the connection
            database_connection.commit()

            return True
        except Exception as e:
            print(f"Error inserting into database: {e}")
            return False
        finally:
            # Close the database connection in the finally block to ensure it is closed
            database_connection.close()
