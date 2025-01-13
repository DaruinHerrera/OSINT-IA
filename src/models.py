import sqlite3

class DBManager:
    def __init__(self, db_name='data.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._crear_tablas() # Create tables
        except sqlite3.Error as e:
            print(f"Error db connection: {e}")
            return False
        return True

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def _crear_tablas(self): #Function to create tables
        if self.cursor:
            try:
                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS frequency (
                    word TEXT PRIMARY KEY,
                    frequency INTEGER
                )
                ''')

                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS rake (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_phrase TEXT UNIQUE
                )
                ''')

                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tfidf (
                    key_phrase TEXT PRIMARY KEY,
                    score_tfidf REAL
                )
                ''')
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error when creating tables: {e}")
                self.conn.rollback() #  Undo changes in case of error

    def save_frequency(self, results):
        if self.cursor:
            for word, frequency in results:
                try:
                    self.cursor.execute("INSERT INTO frequency (word, frequency) VALUES (?, ?)", (word, frequency))
                except sqlite3.IntegrityError:
                    print(f"The word'{word}' already exists in the frequency table.")
            self.conn.commit()

    def save_rake(self, results):
        if self.cursor:
            for key_phrase in results:
                try:
                    self.cursor.execute("INSERT INTO rake (key_phrase) VALUES (?)", (key_phrase,))
                except sqlite3.IntegrityError:
                    print(f"The phrase '{key_phrase}' already in the table rake.")
            self.conn.commit()

    def save_tfidf(self, results):
        if self.cursor:
            for key_phrase, score_tfidf in results:
                try:
                    self.cursor.execute("INSERT INTO tfidf (key_phrase, score_tfidf) VALUES (?, ?)", (key_phrase, score_tfidf))
                except sqlite3.IntegrityError:
                    print(f"The word '{key_phrase}' already in the table tfidf.")
            self.conn.commit()

    def get_datos(self, table):
        if self.cursor:
            try:
                self.cursor.execute(f"SELECT * FROM {table}")
                return self.cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error getting data from the table {table}: {e}")
                return None
        return None