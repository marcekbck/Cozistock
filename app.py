from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime


app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/import', methods=['GET', "POST"])
def import_products(): 
    return render_template('import.html')    
    
@app.route('/inventory', methods=['GET', "POST"])
def inventory():
    sort_by = request.args.get('sort_by', 'expire_date')
    products = get_products(sort_by)
    return render_template('inventory.html', data=products, expire_date_calculator=expire_date_calculator)

def get_products(sort_by='expire_date'):
    valid_columns = ['name', 'quantity', 'price', 'expire_date']
    if sort_by not in valid_columns:
        sort_by = 'name'  # Default value
    conn = sqlite3.connect('products_database.db')
    conn.row_factory = sqlite3.Row  # Acess data as dicts
    cursor = conn.cursor()
    query = f'SELECT * FROM products ORDER BY {sort_by}'
    cursor.execute(query) 
    rows = cursor.fetchall()
    conn.close()
    return rows
    
def expire_date_calculator(expire_date):
    expire_date = datetime.strptime(expire_date, "%Y-%m-%d") # Converte a data de validade para o formato datetime
    today = datetime.today() # Pega a data de hoje
    days_until_expire = (expire_date - today).days # Calcula a diferença entre a data de validade e a data de hoje
    if days_until_expire <= 0:
        color_class = "text-danger"
        days_until_expire = 0
    elif days_until_expire < 7:
        color_class = "text-warning"
    else:
        color_class = "text-success"
    return days_until_expire, color_class
    
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':  #Recover form data
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        expire_date = request.form['expire_date']
        image_path = request.form['image_path']
        
        conn = sqlite3.connect('products_database.db')  # Add product to the database
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, quantity, price, expire_date, image_path)
            VALUES (?, ?, ?, ?, ?)
        """, (name, quantity, price, expire_date, image_path))
        conn.commit()
        conn.close()

        return redirect('/inventory')  # Redirects to inventory page

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

        return redirect('/inventory')

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