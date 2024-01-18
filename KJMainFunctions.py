from KJEntry import KJEntry
import json

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


