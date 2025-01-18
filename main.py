import tkinter as tk
from tkinter import messagebox
import sqlite3
from ObjProduct import Product



conn = sqlite3.connect("products.db")  # Conecta ao banco de dados (ou cria se não existir)
cursor = conn.cursor()

def add_item_widget(): # Função para adicionar o widget de adicionar produto
    list_frame.pack_forget()  # Esconde a lista de produtos

    name_label = tk.Label(add_product_frame, text="Nome do Produto:")       # Criação dos widgets
    name_entry = tk.Entry(add_product_frame)
    quantity_label = tk.Label(add_product_frame, text="Quantidade:")
    quantity_entry = tk.Entry(add_product_frame)
    price_label = tk.Label(add_product_frame, text="Preço:")
    price_entry = tk.Entry(add_product_frame)
    expire_date_label = tk.Label(add_product_frame, text="Data de Validade:")
    expire_date_entry = tk.Entry(add_product_frame)

    add_button = tk.Button(add_product_frame, text="Adicionar", command=lambda: add_item(name_entry, quantity_entry, price_entry, expire_date_entry))

    name_label.grid(row=0, column=0)    # Posicionamento dos widgets
    name_entry.grid(row=0, column=1)
    quantity_label.grid(row=1, column=0)
    quantity_entry.grid(row=1, column=1)
    price_label.grid(row=2, column=0)
    price_entry.grid(row=2, column=1)
    expire_date_label.grid(row=3, column=0)
    expire_date_entry.grid(row=3, column=1)
    add_button.grid(row=4, column=0, columnspan=2)

    add_product_frame.pack(padx=10, pady=10)  # Exibe o frame de criar produto

def add_item(name_entry, quantity_entry, price_entry, expire_date_entry):
    name = name_entry.get()  # Pega o nome do produto
    quantity = quantity_entry.get()  # Pega a quantidade do produto
    price = price_entry.get()  # Pega o preço do produto
    expire_date = expire_date_entry.get()  # Pega a data de validade do produto

    if name != "" and quantity != "" and price != "":       # Verifica se os campos estão preenchidos
        try:
            price = float(price)  # Converte o preço para float
        except ValueError:
            messagebox.showwarning("Preço Inválido", "Por favor, insira um valor numérico para o preço.")
            return
        
        product = Product(id, name, quantity, price, expire_date)           # Criação do objeto Product
        
        cursor.execute('''
            INSERT INTO products (name, quantity, price, expire_date)       
            VALUES (?, ?, ?, ?)
        ''', (product.name, product.quantity, product.price, product.expire_date)) #adiciona os valores no banco de dados
        conn.commit()
        
        show_list_widget() # Chama a função para exibir a lista de produtos

    else:
        messagebox.showwarning("Campos Vazio", "Por favor, preencha todos os campos.")

def show_list_widget(): #Função para exibir a lista de produtos
    add_product_frame.pack_forget()  # Esconde o frame de criar produto
    list_frame.pack(padx=10, pady=10)  # Exibe a lista de produtos
    
    for widget in list_frame.winfo_children():      # Remove todos os widgets dentro de list_frame para evitar duplicação
        widget.destroy()
    
    cursor.execute('SELECT * FROM products')        # Buscar todos os produtos do banco de dados
    products = cursor.fetchall()
    
    products_list = []     # Transformar cada registro em um objeto "obj_product" e adicionar em uma lista
    for p in products:
        obj_product = Product(p[0], p[1], p[2], p[3], p[4])  # Colunas: id, nome, quantidade, preco, validade
        products_list.append(obj_product)
    
    for p in products_list: 
        product_frame = tk.Frame(list_frame, relief=tk.RAISED, borderwidth=1) # Cria um frame para cada produto
        product_frame.pack(fill=tk.X, pady=5)
        
        product_name_label = tk.Label(product_frame, text=f"Nome: {p.name}")
        product_name_label.pack()
        product_quantity_label = tk.Label(product_frame, text=f"Quantidade: {p.quantity}")
        product_quantity_label.pack()
        product_price_label = tk.Label(product_frame, text=f"Preço: {p.price}")
        product_price_label.pack()
        product_expire_date_label = tk.Label(product_frame, text=f"Data de Validade: {p.expire_date}")
        product_expire_date_label.pack()
        update_button = tk.Button(product_frame, text="Edit", command=lambda p=p: update_product(p))
        update_button.pack()
        delete_button = tk.Button(product_frame, text="X", command=lambda p=p, frame=product_frame: delete_product(p.id, frame))
        delete_button.pack()

    return products_list

def update_product(product):
    cursor.execute('''
        UPDATE products
        SET name = ?, quantity = ?, price = ?, expire_date = ?
        WHERE id = ?
    ''', (product.name, product.quantity, product.price, product.expire_date, product.id))
    conn.commit()

def delete_product(product_id, frame):
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    
    frame.destroy()

###################################################################################################
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

# Frame para criar um produto
add_product_frame = tk.Frame(root)

#Botão para adicionar um produto
new_button = tk.Button(header_frame, text="Novo Produto", command=add_item_widget)
new_button.pack(side=tk.LEFT, padx=5)

#Botão para adicionar um produto
import_button = tk.Button(header_frame, text="Importar", command=...)
import_button.pack(side=tk.LEFT, padx=5)

#Botão para adicionar um produto
export_button = tk.Button(header_frame, text="Exportar", command=...)
export_button.pack(side=tk.LEFT, padx=5)

#CHAMA A FUNÇÃO PARA EXIBIR A LISTA DE PRODUTOS
show_list_widget() 
# Rodando a aplicação
root.mainloop()
conn.close()  # Fecha a conexão com o banco de dados