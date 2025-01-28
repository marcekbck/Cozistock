import sqlite3

# SEND TO GROCERYS SITE AND ADD TO BASKET

def export_data_to_txt():
    # Connect to the SQLite database
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    # Fetch all the products from the database
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    # Open the file to write the data
    with open("products_export.txt", "w") as file:
        # Write a header for the file
        file.write("Product List\n")
        file.write("=====================\n")

        # Loop through the products and write them to the file
        for product in products:
            product_data = f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: {product[3]:.2f}€, Expiry Date: {product[4]}, Image Path: {product[5]}\n"
            file.write(product_data)

    # Close the database connection
    conn.close()

    print("Data has been successfully exported to 'products_export.txt'")