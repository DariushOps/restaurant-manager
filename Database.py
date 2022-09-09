import sqlite3


class Database:
    def __init__(self, db):
        self.__db_name = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS [table_menu](
                                [id] INT PRIMARY KEY NOT NULL UNIQUE, 
                                [name] NVARCHAR(50) NOT NULL UNIQUE, 
                                [price] INT NOT NULL, 
                                [is_food] BOOL NOT NULL) WITHOUT ROWID;
                            ''')

        self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS [table_reciepts](
                                [reciept_id] INT NOT NULL,
                                [menu_id] INT NOT NULL REFERENCES [table_menu]([id]),
                                [count] INT,
                                [price] INT) ;
                                 ''')
        self.cursor.execute('''
                            CREATE VIEW IF NOT EXISTS view_menu_reciept AS
                            SELECT table_menu.name,table_reciepts.reciept_id,table_reciepts.count,table_reciepts.price ,
                            (table_reciepts.count * table_reciepts.price) as SUM FROM table_menu
                            INNER JOIN table_reciepts ON table_menu.id == table_reciepts.menu_id;
                            ''')
        self.conn.commit()
        self.conn.close()

    def insert(self, id, name, price, is_food):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('INSERT INTO table_menu VALUES (?,?,?,?)', (id, name, price, is_food))
        self.conn.commit()
        self.conn.close()

    def get_menu_items(self, is_food):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM table_menu WHERE is_food = ? ', (is_food,))
        result = self.cursor.fetchall()
        return result

    def get_max_reciept(self):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT max(reciept_id) FROM table_reciepts')
        result = self.cursor.fetchall()
        return result

    def get_menuName_item(self, menuName_item):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM table_menu WHERE name = ?', (menuName_item,))
        result = self.cursor.fetchall()
        return result

    def reciept_insert(self, reciept_id, menu_id, count, price):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('INSERT INTO table_reciepts VALUES(?,?,?,?)', (reciept_id, menu_id, count, price))
        self.conn.commit()
        self.conn.close()

    def get_reciept_by_recieptid_muneid(self, reciept_id, menu_id):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM table_reciepts WHERE reciept_id = ? and menu_id = ? ', (reciept_id, menu_id))
        result = self.cursor.fetchall()
        return result

    def increase_count(self, reciept_id, menu_id):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('UPDATE table_reciepts set count = count + 1 where reciept_id = ? and menu_id = ?',
                            (reciept_id, menu_id))
        self.conn.commit()
        self.conn.close()

    def get_recieptLoad(self, reciept_id):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM view_menu_reciept WHERE reciept_id = ?  ', (reciept_id,))
        result = self.cursor.fetchall()
        return result

    def delete_rexiept(self,reciept_id,menu_id):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM table_reciepts where reciept_id = ? and menu_id = ?',
                            (reciept_id, menu_id))
        self.conn.commit()
        self.conn.close()

    def decrease_count(self,reciept_id,menu_id):
        self.conn = sqlite3.connect(self.__db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('UPDATE table_reciepts set count = count - 1 where reciept_id = ? and menu_id = ? and count > 0',
                            (reciept_id, menu_id))
        self.conn.execute('DELETE FROM table_reciepts where reciept_id = ? and menu_id = ? and count = 0 ',(reciept_id, menu_id))
        self.conn.commit()
        self.conn.close()
