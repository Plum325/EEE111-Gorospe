import sqlite3
import json
import csv

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
        with open(self.csvFile, "w", newline='') as filehandle:
            csv_writer = csv.writer(filehandle)
            csv_writer.writerow(['Item Name', 'Price', 'Amount', 'Status', 'Order ID'])  # Write header
            dbEntries = self.fetch_items()
            for entry in dbEntries:
                csv_writer.writerow([entry[0], entry[1], entry[2], entry[3], entry[4]])
                
    def export_json(self, filename="Items.json"):
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

    def importCSV(self, filename="Items.csv"):
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    item_name = row['Item Name'].strip()
                    price = row['Price'].strip()
                    amount = row['Amount'].strip()
                    status = row['Status'].strip()
                    order_id = row['Order ID'].strip()

                    self.insert_items(item_name, price, amount, status, order_id)
        except FileNotFoundError:
            print('CSV file not found')
        except Exception as e:
            print(f'Error reading CSV file: {str(e)}')
