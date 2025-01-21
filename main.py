import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from ObjProduct import Product
from datetime import datetime
from PIL import Image, ImageTk



conn = sqlite3.connect("products.db")  # Conecta ao banco de dados (ou cria se não existir)
cursor = conn.cursor()

def add_or_edit_item_widget(is_edit=False, product_id=None, current_name="", current_quantity="", current_price="", current_expire_date=""): # Função para adicionar ou alterar o widget de adicionar produto
    list_frame.pack_forget()  # Esconde a lista de produtos

    name_label = tk.Label(add_product_frame, text="Nome do Produto:")       # Criação dos widgets
    name_entry = tk.Entry(add_product_frame)
    name_entry.insert(0, current_name)
    quantity_label = tk.Label(add_product_frame, text="Quantidade:")
    quantity_entry = tk.Entry(add_product_frame)
    quantity_entry.insert(0, str(current_quantity))
    price_label = tk.Label(add_product_frame, text="Preço:")
    price_entry = tk.Entry(add_product_frame)
    price_entry.insert(0, str(current_price))
    expire_date_label = tk.Label(add_product_frame, text="Data de Validade:")
    expire_date_entry = tk.Entry(add_product_frame)
    expire_date_entry.insert(0, current_expire_date)
    roll_back_button = tk.Button(add_product_frame, text="Voltar", command=show_list_widget)
    roll_back_button.grid(row=4, column=0, columnspan=1)
    
    if hasattr(add_product_frame, 'action_button'):  # Remove o botão de ação antigo, se existir
        add_product_frame.action_button.grid_forget()
        
    if is_edit:
        button_text = "Modificar"
        button_command = lambda: edit_product(product_id, name_entry, quantity_entry, price_entry, expire_date_entry)
    else:
        button_text = "Adicionar"
        button_command = lambda: add_item(name_entry, quantity_entry, price_entry, expire_date_entry)

    action_button = tk.Button(add_product_frame, text=button_text, command=button_command)
    add_product_frame.action_button = action_button  # Salva o botão de ação para remoção posterior
    
    
    name_label.grid(row=0, column=0)    # Posicionamento dos widgets
    name_entry.grid(row=0, column=1)
    quantity_label.grid(row=1, column=0)
    quantity_entry.grid(row=1, column=1)
    price_label.grid(row=2, column=0)
    price_entry.grid(row=2, column=1)
    expire_date_label.grid(row=3, column=0)
    expire_date_entry.grid(row=3, column=1)
    action_button.grid(row=4, column=0, columnspan=2)

    add_product_frame.pack(padx=10, pady=10)  # Exibe o frame de criar produto

def add_item(name_entry, quantity_entry, price_entry, expire_date_entry):
    name = name_entry.get()  # Pega o nome do produto
    quantity = quantity_entry.get()  # Pega a quantidade do produto
    price = price_entry.get()  # Pega o preço do produto
    expire_date = expire_date_entry.get()  # Pega a data de validade do produto

    if name != "" and quantity != "" and price != "":       # Verifica se os campos estão preenchidos
        try:
            quantity = int(quantity)  # Converte a quantidade para int
            price = float(price)  # Converte o preço para float
        except ValueError:
            messagebox.showwarning("Preço Inválido", "Por favor, insira valores numéricos válidos para quantidade e preço.")
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

def show_list_widget():  # Função para exibir a lista de produtos
    add_product_frame.pack_forget()  # Esconde o frame de criar produto
    list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Exibe a lista de produtos

    for widget in list_frame.winfo_children():  # Limpa widgets antigos dentro de list_frame
        widget.destroy()

    cursor.execute('SELECT * FROM products')  # Buscar todos os produtos do banco de dados
    products = cursor.fetchall()

    products_list = []  # Transformar cada registro em um objeto "obj_product" e adiciona em uma lista
    for p in products:
        obj_product = Product(p[0], p[1], p[2], p[3], p[4], p[5])  # Colunas: id, nome, quantidade, preco, validade, imagem
        products_list.append(obj_product)

    row = 0     # Criar frames de produtos
    col = 0
    max_columns = 5  # Ajuste o número máximo de colunas conforme necessário

    for p in products_list:
        product_frame = tk.Frame(list_frame, relief=tk.RAISED, borderwidth=1, bg="#F5F5DC")  # Cria um frame para cada produto
        product_frame.grid(row=row, column=col, padx=5, pady=5, sticky="n")  # Usa grid para organizar os produtos
        
        if not p.image_path:
            p.image_path = "img_example.jpg"  # Imagem padrão caso não exista imagem do produto
        img = Image.open(p.image_path)  # Abre a imagem do produto
        img = img.resize((90, 90), Image.Resampling.LANCZOS)  # Redimensiona a imagem
        img_tk = ImageTk.PhotoImage(img)  # Converte a imagem para o formato tk
        
        image_label = tk.Label(product_frame, image=img_tk)  # Adiciona a imagem no frame do produto
        image_label.image = img_tk  # Mantêm uma referência para a imagem
        image_label.pack(pady=5, padx=5) # Adiciona a imagem no frame do produto

        product_name_label = tk.Label(product_frame, bg="#F5F5DC", text=f"Nome: {p.name}") # Adiciona informações no frame do produto
        product_name_label.pack()
        product_quantity_label = tk.Label(product_frame, bg="#F5F5DC", text=f"Quantidade: {int(p.quantity)}")
        product_quantity_label.pack()
        product_price_label = tk.Label(product_frame, bg="#F5F5DC", text=f"Preço: {round(p.price, 2):.2f}€")
        product_price_label.pack()
        calculated_expire_date = expire_date_calculator(p.expire_date)
        if calculated_expire_date == 0:
            colour = "red"
        elif calculated_expire_date <= 7:
            colour = "orange"
        else:
            colour = "green"
        product_expire_date_label = tk.Label(product_frame, bg="#F5F5DC", text=f"{calculated_expire_date} dias restantes", fg=colour)
        product_expire_date_label.pack()
        
        edit_button = tk.Button(product_frame, text="Editar",font=("Helvetica",6), bg="yellow", command=lambda p=p: add_or_edit_item_widget(
            is_edit=True,
            product_id=p.id,
            current_name=p.name,  # Passa a informação do produto para a função
            current_quantity=p.quantity,
            current_price=p.price,
            current_expire_date=p.expire_date
        ))
        edit_button.pack(side=tk.LEFT, padx=0, pady=0)

        delete_button = tk.Button(product_frame, text="X",font=("Helvetica",6), bg="red", command=lambda p=p, frame=product_frame: delete_product(p.id, frame), width=2, height=1)
        delete_button.pack(side=tk.RIGHT, anchor="se", padx=0, pady=0)

        col += 1   # Controle de posição dos frames na grid
        if col >= max_columns:  # Quando atingir o número máximo de colunas, muda de linha
            col = 0
            row += 1



def edit_product(product_id, name_entry, quantity_entry, price_entry, expire_date_entry):
    # Obter as características do produto a partir da base de dados
    cursor.execute('SELECT name, quantity, price, expire_date FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    # Obter os novos valores (do usuário ou do banco, conforme necessário)
    current_name, current_quantity, current_price, current_expire_date = product

    new_name = name_entry.get() or current_name  # Use o valor do banco se o campo estiver vazio
    new_quantity = int(quantity_entry.get()) if quantity_entry.get() else current_quantity
    new_price = float(price_entry.get()) if price_entry.get() else current_price
    new_expire_date = expire_date_entry.get() or current_expire_date
    
    cursor.execute('''
        UPDATE products
        SET name = ?, quantity = ?, price = ?, expire_date = ?
        WHERE id = ?
    ''', (new_name, new_quantity, new_price, new_expire_date, product_id))
    conn.commit()
    
    show_list_widget()

def delete_product(product_id, frame):
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    
    frame.destroy()

def expire_date_calculator(expire_date):
    expire_date = datetime.strptime(expire_date, "%d-%m-%Y") # Converte a data de validade para o formato datetime
    today = datetime.today() # Pega a data de hoje
    days_until_expire = (expire_date - today).days # Calcula a diferença entre a data de validade e a data de hoje
    if days_until_expire < 0:
        days_until_expire = 0
    return days_until_expire

###################################################################################################
root = tk.Tk() # Criando a janela principal
root.title("Cozistock")
root.geometry("600x600")
root.config(bg="#A8D5BA")

style = ttk.Style()                       # EMBELEZAR
style.configure("TButton",
                relief="flat",           # Sem borda reta
                padding=1,              # Mais espaçamento interno
                font=("Helvetica", 12),
                background="black",    # Cor de fundo
                foreground="black",
                borderwidth=0,
                width=12)

header_frame = tk.Frame(root, bg="#A8D5BA") # Frame superior (cabeçalho com botões de funcionalidades)
header_frame.pack(fill=tk.X, padx=10, pady=20)

line_canvas = tk.Canvas(root, width=600, height=2, bg="#A8D5BA")
line_canvas.create_line(0, 1, 200, 1, fill="black", width=2)  # Linha preta de 2px de espessura
line_canvas.pack(padx=10, pady=5)

list_frame = tk.Frame(root, bg="#A8D5BA") # Frame inferior (onde os produtos serão exibidos)
list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

add_product_frame = tk.Frame(root, bg="#D3D3D3") # Frame para criar um produto

new_button = ttk.Button(header_frame, text="Novo Produto", style="TButton", command=add_or_edit_item_widget)#Botão para adicionar um produto
new_button.pack(side=tk.LEFT, padx=5)

import_button = ttk.Button(header_frame, text="Importar", style="TButton", command=...) #Botão para adicionar um produto
import_button.pack(side=tk.LEFT, padx=5)

export_button = ttk.Button(header_frame, text="Exportar", style="TButton", command=...) #Botão para adicionar um produto
export_button.pack(side=tk.LEFT, padx=5)

#CHAMA A FUNÇÃO PARA EXIBIR A LISTA DE PRODUTOS
show_list_widget() 





root.mainloop() # Rodando a aplicação
conn.close()  # Fecha a conexão com o banco de dados