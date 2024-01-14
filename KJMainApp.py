import customtkinter
import tkinter as tk
from KJMainFunctions import KJMainFunctions
from KJGuiCtk import KJGuiCtk
from KJDatabase import KJDatabase

def main():
    db = KJMainFunctions(init=False, dbName='EmpDb.csv')
    app = KJGuiCtk()
    app.mainloop()

if __name__ == "__main__":
    main()
