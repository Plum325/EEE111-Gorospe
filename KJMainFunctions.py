from KJEntry import KJEntry
from KJDatabase import KJDatabase

class KJMainFunctions:    

    def __init__(self, init=False, dbName='Items.csv'):
        self.database = dict()
        # CSV filename         
        self.dbName = dbName

    def fetch_items(self):
        return [entry.as_tuple() for entry in self.database.values()]

    def insert_item(self, itemName, price, itemNo, status, itemID,):
        newEntry = KJEntry(itemName=itemName, price=price, itemNo=itemNo, status=status, itemID=itemID)
        self.database.update({itemName: newEntry})

        # Print the details as a tuple
        print(newEntry.as_tuple())

    def delete_item(self, itemName):
        self.database.pop(itemName, None)

    def update_item(self, new_price, new_itemNo, new_status, new_itemID, itemName):
        if itemName in self.database:
            entry = self.database[itemName]
            entry.price = new_price
            entry.itemNo = new_itemNo
            entry.status = new_status
            entry.itemID = new_itemID

    def id_exists(self, itemName):
        return itemName in self.database.keys()
    
    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_items()
            for entry in dbEntries:
                filehandle.write(f"Item Name: {entry[1]}\n"
                                 f"Price: {entry[2]}\n"
                                 f"No of Items: {entry[3]}\n"
                                 f"Status: {entry[4]}\n"
                                 f"Product ID: {entry[0]}\n")


