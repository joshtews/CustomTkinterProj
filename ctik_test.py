import queue
import threading
from tkinter import Tk, font, Toplevel
from tkinter import ttk
from pandastable import Table
import pandas as pd
import asyncio

import data_interface as di
from ssh_interface import ssh_interface

class App(Tk):

    #Data Request Thread
    async def update_table(self):
        while True:
            df = await di.update_data(self.table.model.df)
            self.gui_queue.put(df)
            await asyncio.sleep(1)
        
    def update_table_gui(self, df):
        self.table.model.df = df
        self.table.redraw()
        
    def setup_tkinter(self):
        # Set Style
        style = ttk.Style(self)
        self.tk.call('source', 'azure dark 2/azure dark.tcl')
        style.theme_use('azure')

        # Creating a Font object of "TkDefaultFont"
        self.defaultFont = font.nametofont("TkDefaultFont")
  
        # Overriding default-font with custom settings
        # i.e changing font-family, size and weight
        self.defaultFont.configure(family="Roboto",
                                   size=19)
        
        # configure window
        self.title("Test Browser")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

    def setup_unconnected_sidebar(self):
        # create sidebar frame with Buttons
        self.sidebar_frame = ttk.LabelFrame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ttk.Label(self.sidebar_frame, text="Test Browser")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ttk.Button(self.sidebar_frame, text="Connect", command=self.connect_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
    def setup_connected_sidebar(self):
        # create sidebar frame with Buttons
        self.sidebar_frame = ttk.LabelFrame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ttk.Label(self.sidebar_frame, text="Test Browser")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ttk.Button(self.sidebar_frame, text="Remove Selected", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ttk.Button(self.sidebar_frame, text="Request Element", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        
        #add disconnect button at the bottom of the frame
        self.sidebar_button_3 = ttk.Button(self.sidebar_frame, text="Disconnect", command=self.disconnect_button_event)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10, sticky="s")

    def setup_table(self):
        # Right Frame
        self.right_frame = ttk.Frame(self)
        self.right_frame.grid(row=0, rowspan=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
        df = di.create_sample_data()
        self.table = pt = Table(self.right_frame, dataframe=df,
                                showtoolbar=False, showstatusbar=False,
                                maxcellwidth=1500)
        pt.cellbackgr = "grey25"
        pt.grid_color = "grey75"
        pt.textcolor =  "#f2eeeb"
        pt.rowselectedcolor = "#389cfc"
        pt.show()
        
        pt.rowheader.grid_forget()
        pt.rowindexheader.grid_forget()
        
        pt.redraw()

    def __init__(self, parent=None):
        super().__init__()
        
        # Setup Style Elements
        self.setup_tkinter()
        
        # Setup Sidebar
        self.setup_unconnected_sidebar()
        
        # Setup Table
        self.setup_table()
        
        # Bind Mouse Click Events
        self.bind('<Button-1>',self.handle_left_click)
        self.bind("<ButtonRelease-1>", self.handle_left_release)
        self.left_click_held = False
        
        self.ssh = ssh_interface()
        self.gui_queue = queue.Queue()
        #Create Loop Thread
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self.update_table())

        return

    def handle_left_click(self, event):
        self.left_click_held = True
        print("left click")
        
    def handle_left_release(self, event):
        self.left_click_held = False
        print("left release")
    
    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def connect_button_event(self):
        # Toplevel object which will
        # be treated as a new window
        self.connectWindow = Toplevel(self)
    
        # sets the title of the
        # Toplevel widget
        self.connectWindow.title("Connect")
    
        # sets the geometry of toplevel
        self.connectWindow.geometry("500x500")
    
        # Creating widgets
        connect_label = ttk.Label(self.connectWindow, text="Conenct to Server")
        host_label = ttk.Label(self.connectWindow, text="Host")
        self.host_entry = ttk.Entry(self.connectWindow,)
        username_label = ttk.Label(self.connectWindow, text="Username")
        self.username_entry = ttk.Entry(self.connectWindow,)
        password_label = ttk.Label(self.connectWindow, text="Password")
        self.password_entry = ttk.Entry(self.connectWindow, show="*")
        login_button = ttk.Button( self.connectWindow, text="Connect", command=self.attemp_connect)

        # Placing widgets on the screen
        connect_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        host_label.grid(row=1, column=0)
        self.host_entry.grid(row=1, column=1, pady=20)
        username_label.grid(row=2, column=0)
        self.username_entry.grid(row=2, column=1, pady=20)
        password_label.grid(row=3, column=0)
        self.password_entry.grid(row=3, column=1, pady=20)
        login_button.grid(row=4, column=0, columnspan=2, pady=30)
        
    def disconnect_button_event(self):
        self.ssh.disconnect()
        self.sidebar_frame.destroy()
        self.setup_unconnected_sidebar()
        #Stop Loop Thread
        self.loop.call_soon_threadsafe(self.loop.stop)
        
    def attemp_connect(self):
        self.ssh.connect(self.host_entry.get(), 8080, self.username_entry.get(), self.password_entry.get() ) 
        if self.ssh.is_connected:
            self.connectWindow.destroy()
            self.sidebar_frame.destroy()
            self.setup_connected_sidebar()
            #Start Loop Thread
            threading.Thread(target=self.loop.run_forever).start()

    
    def update_cycle(self):
        
        app.after(500,app.update_cycle)
        
        if self.ssh.is_connected:
            #done update while mousing is being held down to prevent lag
            if self.left_click_held:
                return
            try:
                df = app.gui_queue.get_nowait()
                self.update_table_gui(df)
            except queue.Empty:
                pass

if __name__ == "__main__":
    app = App()
    app.after(500,app.update_cycle)
    app.mainloop()