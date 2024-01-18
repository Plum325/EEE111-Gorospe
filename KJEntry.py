class KJEntry:
    def __init__(self,
                 itemName = "Select Food",
                 itemNo = 1,
                 price = 0,
                 status = "Dine In",
                 itemID = 1):
        self.itemName = itemName
        self.price = price
        self.itemNo = itemNo
        self.status = status
        self.itemID = itemID

    def as_tuple(self):
        return (self.itemName, self.price, self.itemNo, self.status, self.itemID)