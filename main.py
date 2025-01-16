import tkinter as tk
from tkinter import messagebox

# Função para adicionar um item
def add_item_widget():
    # Se o frame de adicionar produto estiver visível, escondê-lo
    if add_product_frame.winfo_ismapped():
        return  # O formulário já está visível, não faz sentido mostrá-lo novamente

    add_product_frame.pack(fill=tk.X, pady=5)  # Mostra o frame de adicionar produto

def add_item(name_entry, quantity_entry, price_entry):
    item_name = name_entry.get()  # Pega o nome do produto
    item_quantity = quantity_entry.get()  # Pega a quantidade do produto
    item_price = price_entry.get()  # Pega o preço do produto

    # Verifica se os campos estão preenchidos
    if item_name != "" and item_quantity != "" and item_price != "":
        # Cria um frame para o item
        frame_item = tk.Frame(list_frame)
        frame_item.pack(fill=tk.X, pady=5)

        # Exibe as informações do item no frame
        tk.Label(frame_item, text=f"Produto: {item_name}").pack(side=tk.LEFT, padx=5)
        tk.Label(frame_item, text=f"Quantidade: {item_quantity}").pack(side=tk.LEFT, padx=5)
        tk.Label(frame_item, text=f"Preço: € {item_price}").pack(side=tk.LEFT, padx=5)

        # Botão para remover o item
        btn_remover = tk.Button(frame_item, text="Remover", command=lambda: remover_item(frame_item))
        btn_remover.pack(side=tk.RIGHT, padx=5)

        # Limpa os campos de entrada
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

        # Esconde o formulário de entrada após a inserção do item
        add_product_frame.pack_forget()
    else:
        messagebox.showwarning("Campos Vazio", "Por favor, preencha todos os campos.")

# Função para remover um item
def remover_item(frame_item):
    frame_item.destroy()  # Remove o frame do item da lista

# Criando a janela principal
root = tk.Tk()
root.title("Cozistock")
root.geometry("800x600")

# Frame superior (cabeçalho com botões de funcionalidades)
header_frame = tk.Frame(root)
header_frame.pack(fill=tk.X, padx=10, pady=10)

# Frame inferior (onde os produtos serão exibidos)
list_frame = tk.Frame(root)
list_frame.pack(padx=10, pady=10)

# Frame para adicionar um item (criado uma única vez)
add_product_frame = tk.Frame(root)

# Campo de entrada para o nome do produto
name_entry = tk.Entry(add_product_frame, width=20)
name_entry.pack(pady=5)

# Campo de entrada para a quantidade do produto
quantity_entry = tk.Entry(add_product_frame, width=5)
quantity_entry.pack(pady=5)

# Campo de entrada para o preço do produto
price_entry = tk.Entry(add_product_frame, width=5)
price_entry.pack(pady=5)

# Botão para adicionar o item
add_btn = tk.Button(add_product_frame, text="Adicionar", command=lambda: add_item(name_entry, quantity_entry, price_entry))
add_btn.pack(pady=5)

# Botões de funcionalidades na parte superior
add_btn_top = tk.Button(header_frame, text="Adicionar Item", command=add_item_widget)
add_btn_top.pack(side=tk.LEFT, padx=5)

# Rodando a aplicação
root.mainloop()
