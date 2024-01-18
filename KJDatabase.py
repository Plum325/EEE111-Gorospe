import sqlite3
import json

class KJDatabase:
    def __init__(self, dbName='Items.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.jsonFile = self.dbName.replace('.db', '.json')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Items (
                itemName TEXT PRIMARY KEY,
                price TEXT,
                itemNo TEXT,
                status TEXT,
                itemID TEXT)''')

        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

    def commit_close(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Items (
                itemName TEXT PRIMARY KEY,
                price TEXT,
                itemNo TEXT,
                status TEXT,
                itemID TEXT)''')
        self.connect_cursor()
        self.commit_close()

    def fetch_items(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Items')
        items = self.cursor.fetchall()
        self.conn.close()
        return items

    def insert_items(self, itemName, price, itemNo, status, itemID):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Items (itemName, price, itemNo, status, itemID) VALUES (?, ?, ?, ?, ?)',
                            (itemName, price, itemNo, status, itemID))
        self.commit_close()

    def delete_items(self, itemName):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Items WHERE itemName = ?', (itemName,))
        self.commit_close()

    def update_items(self, new_price, new_itemNo, new_status, new_itemID, itemName):
        self.connect_cursor()
        self.cursor.execute('UPDATE Items SET price = ?, itemNo = ?, status = ?, itemID = ? WHERE itemName = ?',
                            (new_price, new_itemNo, new_status, new_itemID, itemName))
        self.commit_close()

    def itemName_exists(self, itemName):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Items WHERE itemName = ?', (itemName,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.dbName, "w") as filehandle:
            dbEntries = self.fetch_items()
            for entry in dbEntries:
                filehandle.write(f"Order ID: {entry[4]}\n"
                                 f"Item Name: {entry[0]}\n"
                                 f"Price: {entry[1]}\n"
                                 f"No of Items: {entry[2]}\n"
                                 f"Status: {entry[3]}\n\n"
                                 )
                
    def export_json(self, filename="data.json"):
        items = self.fetch_items()
        json_data = []
        for item in items:
            item_dict = {
                "Order ID": item[4],
                "Item Name": item[0],
                "Price": item[1],
                "Amount": item[2],
                "Status": item[3],
            }
            json_data.append(item_dict)

        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)
