from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__) # inicia app

# Conexão com o banco de dados

import sqlite3

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/import', methods=['GET', "POST"])
def import_products(): 
    return render_template('import.html')         # isto só encaminha para a pagina certa 
    
@app.route('/inventory', methods=['GET', "POST"])
def inventory():
    sort_by = request.args.get('sort_by', 'expire_date')
    products = get_products(sort_by)
    return render_template('inventory.html', data=products)

def get_products(sort_by='expire_date'):
    valid_columns = ['name', 'quantity', 'price', 'expire_date']
    if sort_by not in valid_columns:
        sort_by = 'name'  # Valor padrão
    conn = sqlite3.connect('products_database.db')
    conn.row_factory = sqlite3.Row  # Permite acessar os dados como dicionários
    cursor = conn.cursor()
    query = f'SELECT * FROM products ORDER BY {sort_by}'
    cursor.execute(query)  # Consulta à tabela products
    rows = cursor.fetchall()
    conn.close()
    return rows
    
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Recupera dados do formulário
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        expire_date = request.form['expire_date']
        image_path = request.form['image_path']

        # Adiciona produto à base de dados
        conn = sqlite3.connect('products_database.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, quantity, price, expire_date, image_path)
            VALUES (?, ?, ?, ?, ?)
        """, (name, quantity, price, expire_date, image_path))
        conn.commit()
        conn.close()

        return redirect('/inventory')  # Redirecionar para a página de inventário
    return render_template('add_product.html')  # Renderiza o template de adição de produto
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])

def edit_product(product_id):
    conn = sqlite3.connect('products_database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Update the product information
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        expire_date = request.form['expire_date']
        
        cursor.execute("""
            UPDATE products
            SET name = ?, quantity = ?, price = ?, expire_date = ?
            WHERE id = ?
        """, (name, quantity, price, expire_date, product_id))
        conn.commit()
        conn.close()

        return redirect(url_for('inventory'))

    # Retrieve product details for editing
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()

    return render_template('edit_product.html', product=product)

@app.route('/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    conn = sqlite3.connect('products_database.db')  # For accessing products
    conn.row_factory = sqlite3.Row  # Ensures rows are accessed as dictionaries
    cursor = conn.cursor()

    # Archive product
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    if product is None:
        conn.close()
        return "Product not found", 404

    # Connect to the archive database (separate from products)
    archive_conn = sqlite3.connect('archive.db')
    archive_cursor = archive_conn.cursor()
    archive_cursor.execute("""
        CREATE TABLE IF NOT EXISTS archive (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            price REAL,
            expire_date TEXT,
            image_path TEXT
        )
    """)
    archive_cursor.execute("""
        INSERT INTO archive (name, quantity, price, expire_date, image_path)
        VALUES (?, ?, ?, ?, ?)
    """, (product['name'], product['quantity'], product['price'], product['expire_date'], product['image_path']))
    
    archive_conn.commit()
    archive_conn.close()

    # Delete product from products table
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('inventory'))

@app.route('/archive')
def archive():
    # Connect to the archive database
    conn = sqlite3.connect('archive.db')
    conn.row_factory = sqlite3.Row  # Allows accessing rows like dictionaries
    cursor = conn.cursor()

    # Fetch all products from the archive table
    cursor.execute("SELECT * FROM archive")
    archived_products = cursor.fetchall()

    # Close the connection
    conn.close()

    # Render the archive template and pass the archived products
    return render_template('archive.html', archive=archived_products)


@app.route('/export', methods=['GET', "POST"])
def export_products():
    return render_template('export.html')
    
@app.route('/login', methods=['GET', "POST"])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)