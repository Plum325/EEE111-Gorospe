from KJEntry import KJEntry
import json
import csv

class KJMainFunctions:    

    def __init__(self, init=False, dbName='Items.csv'):
        self.dbName = dbName
        
        self.database = dict()

    def fetch_items(self):
        return [entry.as_tuple() for entry in self.database.values()]

    def insert_items(self, itemName, price, itemNo, status, itemID,):
        newEntry = KJEntry(itemName=itemName, price=price, itemNo=itemNo, status=status, itemID=itemID)
        self.database.update({itemName:newEntry})

    def delete_items(self, itemName):
        self.database.pop(itemName)

    def update_items(self, new_price, new_itemNo, new_status, new_itemID, itemName):
        if itemName in self.database:
            entry = self.database[itemName]
            entry.price = new_price
            entry.itemNo = new_itemNo
            entry.status = new_status
            entry.itemID = new_itemID
    
    def itemName_exists(self, itemName):
        return itemName in self.database.keys()
    
    def export_csv(self):
        with open("Items.csv", "w", newline='') as filehandle:
            csv_writer = csv.writer(filehandle)
            csv_writer.writerow(['Item Name', 'Price', 'Amount', 'Status', 'Order ID'])
            dbEntries = self.fetch_items()
            for entry in dbEntries:
                csv_writer.writerow([entry[0], entry[1], entry[2], entry[3], entry[4]])
                
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
