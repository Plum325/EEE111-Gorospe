import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from KJDatabase import KJDatabase

class KJGuiCtk(customtkinter.CTk):
    def __init__(self,database = KJDatabase("Items.db")):
        super().__init__()
        self.db = database
        
        #   Main Options
        self.title("Kainan ni Joshua - Order Register")
        self.geometry("1350x450")
        self.config(bg="#FFE8C2")
        self.resizable(False, False)

        self.font1 = ('Monospace Text', 20, 'bold')
        self.font2 = ('Mono Upper', 12, 'bold')

        #   Menu and the Combo Box
        self.itemName = self.newCtkLabel("Menu")
        self.itemName.place(x=10, y=10)
        self.itemNameVar = StringVar()
        self.itemNameOptions = ["Adobong Manok", "Chicken Curry", "Buttered Shrimp", "Sinigang na Baboy",
                                "Tinolang Manok", "Fried Chicken"]
        self.itemNameCBox = self.newCtkComboBox(options=self.itemNameOptions,
                                                 entryVariable=self.itemNameVar)
        self.itemNameCBox.place(x=110, y=10)

        #   Price and Entry
        self.price = self.newCtkLabel("Price")
        self.price.place(x=10, y=60)
        self.priceEntry = self.newCtkEntry(state=DISABLED)
        self.priceEntry.bind("<Button-1>", self.priceAdminWindow)
        self.priceEntry.place(x=110, y=60)
        self.priceAdminWindowOpened = False

        #   Amount and Entry
        self.itemNo = self.newCtkLabel("Amount")
        self.itemNo.place(x=10,y=110)
        self.itemNoEntry = self.newCtkEntry(state=NORMAL)
        self.itemNoEntry.place(x=110,y=110)

        #   Status and the Combo Box
        self.status = self.newCtkLabel("Status")
        self.status.place(x=10,y=160)
        self.statuscboxVar = StringVar()
        self.statuscboxOptions = ["Dine In", "Take-out"]
        self.statuscbox = self.newCtkComboBox(self.statuscboxOptions,self.statuscboxVar)
        self.statuscbox.place(x=110,y=160)

        #   Product ID and Entry
        self.itemID = self.newCtkLabel("Prd ID")
        self.itemID.place(x=10, y=210)
        self.itemIDEntry = self.newCtkEntry(state=DISABLED)
        self.itemIDEntry.bind("<Button-1>", self.itemIDAdminWindow)
        self.itemIDEntry.place(x=110, y=210)
        self.itemIDAdminWindowOpened = False

        # 3F4B3B - Dark Green, 44633F - Forest Green, FFE8C2 - Wheat, 5CAB7D - Mint Green, A1683A - Brown

        #   Buttons
        self.addButton = self.newCtkButton(text='Add Product',
                                onClickHandler=self.addEntry,
                                fgColor='#3F4B3B',
                                hoverColor='#5CAB7D',
                                borderColor='#3F4B3B')
        self.addButton.place(x=50,y=260)

        self.updateButton = self.newCtkButton(text='Update Product',
                                    onClickHandler=self.update_entry)
        self.updateButton.place(x=50,y=310)

        self.deleteButton = self.newCtkButton(text='Void Product',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#A1683A',
                                    hoverColor='#3F4B3B',
                                    borderColor='#A1683A')
        self.deleteButton.place(x=50,y=360)

        self.exporttoCSVButton = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.exporttoCSVButton.place(x=50,y=410)

        self.exporttoJSONButton = self.newCtkButton(text='Export to JSON',
                                    onClickHandler=self.export_to_json)
        self.exporttoJSONButton.place(x=250,y=410)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('default')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#5CAB7D',
                        background='#FFE8C2',
                        fieldlbackground='#A1683A')

        self.style.map('Treeview', background=[('selected', '#44633F')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Product ID', 'Item Name', 'Price', 'Amount', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Product ID', anchor=tk.CENTER, width=10)
        self.tree.column('Item Name', anchor=tk.CENTER, width=150)
        self.tree.column('Price', anchor=tk.CENTER, width=150)
        self.tree.column('Amount', anchor=tk.CENTER, width=10)
        self.tree.column('Status', anchor=tk.CENTER, width=150)

        self.tree.heading('Product ID', text='Product ID')
        self.tree.heading('Item Name', text='Item Name')
        self.tree.heading('Price', text='Price')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=320, y=10, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    def newCtkEntry(self, state):
        widgetState = state
        widget = customtkinter.CTkEntry(self,
                                        font=self.font2,
                                        text_color="#FFE8C2",
                                        fg_color="#5CAB7D",
                                        border_color="#3F4B3B",
                                        border_width=1,
                                        width=200,
                                        state=widgetState,
                                        )
        return widget

    def newCtkLabel(self, text="NewLabel"):
        widget = customtkinter.CTkLabel(self,
                                        text=text,
                                        font=self.font1,
                                        text_color="#44633F",
                                        bg_color="#FFE8C2")
        return widget

    def newCtkComboBox(self, options=[], entryVariable=None):
        widget = customtkinter.CTkComboBox(self,
                                           font=self.font2,
                                           text_color="#FFE8C2",
                                           fg_color="#5CAB7D",
                                           border_color="#3F4B3B",
                                           width=200,
                                           variable=entryVariable,
                                           values=options,
                                           state='readonly')

        widget.set(options[0])
        return widget

    # 3F4B3B - Dark Green, 44633F - Forest Green, FFE8C2 - Wheat, 5CAB7D - Mint Green, A1683A - Brown

    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#3F4B3B', hoverColor='#5CAB7D', bgColor='#44633F', borderColor='#3F4B3B'):
        textColor = "#FFE8C2"
        fgColor=fgColor
        hoverColor=hoverColor
        bgColor=bgColor
        borderColor=borderColor
        function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=function,
                                        font=self.font1,
                                        text_color=textColor,
                                        fg_color=fgColor,
                                        hover_color=hoverColor,
                                        bg_color=bgColor,
                                        border_color=borderColor,
                                        border_width=1,
                                        cursor="hand2",
                                        corner_radius=10,
                                        width=150)
       
        return widget

    def priceAdminWindow(self, event):
        if not self.priceAdminWindowOpened:
            adminWindow = Toplevel(self)
            adminWindow.title("Change Price")
            adminWindow.geometry("300x50")
            passwordEntry = Entry(adminWindow, show="*")
            passwordEntry.pack()
            submitButton = Button(adminWindow, text="Submit", command=lambda: self.priceSubmitPassword(passwordEntry, adminWindow))
            submitButton.pack()
            
    def priceSubmitPassword(self, password_entry, adminWindow):
        entered_password = password_entry.get()
        if entered_password == "111":
            adminWindow.destroy()
            self.priceAdminWindowOpened = True
            self.priceEntry.configure(state=NORMAL)
            
        else:
            messagebox.showerror("Wrong Password","Incorrect password")

    def itemIDAdminWindow(self, event):
        if not self.itemIDAdminWindowOpened:
            adminWindow = Toplevel(self)
            adminWindow.title("Change Product ID")
            adminWindow.geometry("300x50")
            passwordEntry = Entry(adminWindow, show="*")
            passwordEntry.pack()
            submitButton = Button(adminWindow, text="Submit", command=lambda: self.itemIDSubmitPassword(passwordEntry, adminWindow))
            submitButton.pack()
            
    def itemIDSubmitPassword(self, password_entry, adminWindow):
        entered_password = password_entry.get()
        if entered_password == "111":
            adminWindow.destroy()
            self.itemIDAdminWindowOpened = True
            self.itemIDEntry.configure(state=NORMAL)
            
        else:
            messagebox.showerror("Wrong Password","Incorrect password")

    def addEntry(self):
        itemID=self.itemIDEntry.get()
        itemName=self.itemNameVar.get()
        price=self.priceEntry.get()
        itemNo=self.itemNoEntry.get()
        status=self.statuscboxVar.get()

        if not (itemID and itemName and price and itemNo and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(itemID):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_items(itemID, itemName, price, itemNo, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    # Handles
    def add_to_treeview(self):
        items = self.db.fetch_items()
        self.tree.delete(*self.tree.get_children())
        for item in items:
            print(item)
            self.tree.insert('', END, values=item)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.itemIDEntry.delete(0, END)
        self.priceEntry.delete(0, END)
        self.itemNameVar.set('Adobong Manok')
        self.itemNoEntry.delete(0, END)
        self.statuscboxVar.set('Dine in')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.itemNameVar.set(row[1])
            self.priceEntry.insert(0, row[2])
            self.itemNoEntry.insert(0, row[3])
            self.statuscboxVar.set(row[4])
            self.itemIDEntry.insert(0, row[0])
        else:
            pass

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a product to delete')
        else:
            itemID = self.itemIDEntry.get()
            self.db.delete_items(itemID)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Choose a product to update")
        else:
            itemName = self.itemNameVar.get()
            price = self.priceEntry.get()
            itemNo = self.itemNoEntry.get()
            status = self.statuscboxVar.get()
            itemID = self.itemIDEntry.get()
            self.db.update_items(itemName, price, itemNo, status, itemID)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo("Success", "Data has been updated")


    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo("Success", f"Data exported to {self.db.dbName}.csv")

    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo("Success", f"Data Exported to {self.db.dbName}.json")

if __name__ == "__main__":
    app = KJGuiCtk()
    app.mainloop()
