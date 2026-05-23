import customtkinter as ctk
from Login import Login
from Menu import Menu
from Inventaire import Inventaire

ctk.set_default_color_theme("green")

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.geometry("625x625")
        self.current_frame = None
        self.current_user = None
        self.show_frame("login")

    def show_frame(self, page):
        if self.current_frame:
            self.current_frame.destroy()

        if page == "login":
            self.current_frame = Login(self, self.show_frame)

        elif page == "menu":
            self.current_frame = Menu(self, self.show_frame)
        
        elif page == "inventaire":
            self.current_frame = Inventaire(self, self.show_frame)

        self.current_frame.pack(fill="both", expand=True)

app = App()
app.mainloop()
