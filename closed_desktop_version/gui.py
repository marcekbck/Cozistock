import customtkinter as ctk
from PIL import Image, ImageTk

# Inicializar a janela
root = ctk.CTk()
root.geometry("600x400")

# Frame principal
main_frame = ctk.CTkFrame(root, fg_color="blue")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

bg_image = Image.open("bg_test.jpg")  # Abre a imagem de fundo
bg_ctk_image = ctk.CTkImage(light_image=bg_image, size=(600, 600))  # Converte para CTkImage e redimensiona
bg_label = ctk.CTkLabel(main_frame, image=bg_ctk_image, text="")  # Adiciona a imagem no CTkLabel
bg_label.grid(row=0, column=0, rowspan=10, columnspan=10, sticky="nsew")  # Ajusta a imagem para preencher a janela

# Adicionar os botões lado a lado no topo
button1 = ctk.CTkButton(main_frame, text="Button 1", fg_color="red", corner_radius=20, bg_color="transparent")
button1.grid(row=0, column=0, padx=5, pady=5)

button2 = ctk.CTkButton(main_frame, text="Button 2", fg_color="blue", corner_radius=20)
button2.grid(row=0, column=1, padx=5, pady=5)

button3 = ctk.CTkButton(main_frame, text="Button 3", fg_color="green", corner_radius=20)
button3.grid(row=0, column=2, padx=5, pady=5)

# Linha horizontal separadora
line_break = ctk.CTkLabel(main_frame, text="----------------------", fg_color="transparent")
line_break.grid(row=1, column=0, columnspan=3, pady=10)

# Adicionar os produtos lado a lado
for i in range(5):
    product = ctk.CTkButton(main_frame, text=f"Product {i + 1}", fg_color="orange", corner_radius=20)
    product.grid(row=2, column=i, padx=5, pady=5)  # Produtos lado a lado

root.mainloop()