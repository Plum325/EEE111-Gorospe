from KJMainFunctions import KJMainFunctions
from KJGuiCtk import KJGuiCtk

def main():
    db = KJMainFunctions(init=False, dbName='Items.csv')
    app = KJGuiCtk(database=db)
    app.mainloop()

if __name__ == "__main__":
    main()

