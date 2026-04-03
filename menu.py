import customtkinter as ctk

class Menu(ctk.CTkFrame):
    def __init__(self, master, switch_page):
        super().__init__(master)

        self.switch_page = switch_page
        
        self.frame = ctk.CTkFrame(self, width=500, height=300, corner_radius=10)
        self.frame.pack(pady=40)

        self.label = ctk.CTkLabel(self.frame, text="FOODTROC", font=("Segoe UI", 30))
        self.label.grid(row=0, column=0, columnspan=2, pady=(10,20))

        self.button = ctk.CTkButton(self.frame,text="Déconnexion",command=self.logout)
        self.button.grid(row=3, column=0, columnspan=2, pady=20)

    def logout(self):
        self.switch_page("login")