from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__) # inicia app

@app.route('/home', methods=['GET'])
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

@app.route('/export', methods=['GET', "POST"])
def export_products():
    return render_template('export.html')
    
@app.route('/login', methods=['GET', "POST"])
def login():
    return render_template('login.html')





if __name__ == '__main__':
    app.run(debug=True)