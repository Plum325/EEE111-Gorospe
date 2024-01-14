import sqlite3
import json

class KJDatabase:
    def __init__(self, dbName='Items.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        self.create_table()  # Ensure the table is created during initialization
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

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

    def commit_close(self):
        self.conn.commit()
        self.conn.close()

    def fetch_items(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Items')
        items = self.cursor.fetchall()
        self.commit_close()
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

    def update_items(self, new_price, new_itemNo, new_status,  new_itemID, itemName):
        self.connect_cursor()
        self.cursor.execute('UPDATE Items SET price = ?, itemNo = ?, status = ?, itemID = ? WHERE itemName = ?',
                    (new_itemID, new_price, new_itemNo, new_status, itemName))
        self.commit_close()

    def id_exists(self, itemName):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Items WHERE itemName = ?', (itemName,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_items()
            for entry in dbEntries:
                filehandle.write(f"Item Name: {entry[1]}\n"
                                 f"Price: {entry[2]}\n"
                                 f"No of Items: {entry[3]}\n"
                                 f"Status: {entry[4]}\n"
                                 f"Product ID: {entry[0]}\n")
                
    def export_json(self, filename="data.json"):
        items = self.fetch_items()
        json_data = []
        for item in items:
            item_dict = {
                "Product ID": item[0],
                "Item Name": item[1],
                "Price": item[2],
                "Amount": item[3],
                "Status": item[4]
            }
            json_data.append(item_dict)

        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)
