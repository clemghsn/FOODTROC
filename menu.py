import customtkinter as ctk
from PIL import Image

class Menu(ctk.CTkFrame):
    def __init__(self, master, switch_page):
        super().__init__(master)

        # image
        self.img_home = ctk.CTkImage(light_image=Image.open("images/home.png"),size=(40,40))
        self.img_add = ctk.CTkImage(light_image=Image.open("images/add.png"),size=(40,40))
        self.img_map = ctk.CTkImage(light_image=Image.open("images/map.png"),size=(40,40))
        self.img_foodtroc= ctk.CTkImage(light_image=Image.open("images/foodtroc.png"),size=(300,100))
        self.switch_page = switch_page
        
        self.frame = ctk.CTkFrame(self, width=500, height=300, corner_radius=10)
        self.frame.pack(pady=40)

        for i in range(4):
            self.frame.grid_columnconfigure(i, weight=1)

        self.label = ctk.CTkLabel(self.frame, text="",image = self.img_foodtroc )
        self.label.grid(row=0, column=0, columnspan=4, pady=(10,20))

        self.button_home = ctk.CTkButton(self.frame, text="", image = self.img_home, width=50, height=50, fg_color ="transparent", border_width=0)
        self.button_home.grid(row=1, column=0, padx=10, pady=20, sticky="ew")

        self.button_add = ctk.CTkButton(self.frame, text="", image = self.img_add, width=50, height=50, fg_color ="transparent", border_width=0)
        self.button_add.grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        self.button_carte = ctk.CTkButton(self.frame,text="", image = self.img_map, width=50, height=50, fg_color ="transparent", border_width=0)
        self.button_carte.grid(row=1, column=2, padx=10, pady=20, sticky="ew")

        self.button_logout = ctk.CTkButton(self.frame, text="Déconnexion", command=self.logout)
        self.button_logout.grid(row=1, column=3, padx=10, pady=20, sticky="ew")

    def logout(self):
        self.switch_page("login")