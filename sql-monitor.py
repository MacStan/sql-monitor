import datetime
import pyodbc
import time

from tkinter import Tk, Label, Button, Frame, Listbox, END, Entry

class MyFirstGUI:
    def __init__(self, tkRoot):
        self.tkRoot = tkRoot

        self.con = pyodbc.connect(driver="{SQL Server}", server=".", database="DomoticaDB")
        self.dbCmd = "SELECT * FROM [dbo].[Items]"
                
        tkRoot.title("SQL monitor")
        # Top Frame --- --- ---
        self.labelsFrame = Frame(tkRoot)
        self.labelsFrame.pack(fill="both", expand ='YES')

        self.listbox = Listbox(self.labelsFrame)
        self.listbox.pack(fill="both", expand ='YES')
        self.listbox.config(font = 'Consolas', justify = 'center')

        # Bottom Frame --- --- ---
        self.bottomFrame = Frame(tkRoot)
        self.bottomFrame.pack(fill="both", expand ='YES')
                     
        self.label = Label(self.bottomFrame, text="Placeholder")
        self.label.pack(side = "left", expand = 'yes')

        self.entry = Entry(self.bottomFrame, width = 0)
        self.entry.insert(0, self.dbCmd)
        self.entry.pack(side = "left", expand = 'yes')
        
        # Root Frame --- --- ---
        self.greet_button = Button(tkRoot, text="Update Query", command=self.update_query)
        self.greet_button.pack()

        self.close_button = Button(tkRoot, text="Close", command=tkRoot.quit)
        self.close_button.pack()
        
        self.tkRoot.after(1000, self.update)

    def update_query(self):
        self.label.configure( text = self.entry.get() )
        self.dbCmd = self.entry.get()



    def update(self):
        msg = self.get_sql(self.dbCmd)
        self.listbox.delete(0,END)
        [self.listbox.insert(END, item) for item in msg]
        
        for each in range(0, self.listbox.size() ):
            self.listbox.itemconfig(each,bg = self.tkRoot['bg'])

        self.listbox.config(width=0)
        self.tkRoot.after(1000, self.update)

        #self.entry.delete(0, "end")
        #self.entry.insert(0, self.dbCmd)


    def get_sql(self, cmd):
        cur = self.con.cursor()
        res = cur.execute(cmd)

        ret = []
        for r in res:
            for each in [0,3,4]:
                if(r[each] is None):
                    r[each] = ""
            ret.append(  f"Id: {r[0]:>10} \tName: {r[3][:20] : <25} \tNice name: {r[4][:20]:<25}")#" \tknown_device_id: {r[10]}")

            # if( "zwave" in r[4]):
            #     if(r[3] is not None and r[9] is not None):
            #         ret.append()
            #     else:
            #         if r[3] is None:
            #             r[3] = "None"
            #         if r[9] is None:
            #             r[9] = "None"
            #         ret.append(f"Id: {r[0]} \tName: {r[3][:20]:<25} \tNice name: {r[9][:20]:<25} \tknown_device_id: {r[11]}")
        return ret
        
root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()