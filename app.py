import sqlite3
from pathlib import Path
import os
from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)


def get_db_connection():
    db = Path(__file__).parent / "Cepumkaste.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("products.html", products=products)


@app.route("/product/<int:product_id>")
def products_show(product_id):
    conn = get_db_connection()
    product = conn.execute(
        """
        SELECT 
            products.*, 
            producers.name AS producer_name,
            shops.name AS shop_name,
            dipping_quality.dipping_quality AS dip_quality
        FROM products
        LEFT JOIN producers ON products.producer_id = producers.id
        LEFT JOIN shops ON products.shop_id = shops.id
        LEFT JOIN dipping_quality ON products.dip_id = dipping_quality.id
        WHERE products.id = ?
        """,
        (product_id,)
    ).fetchone()
    conn.close()

    return render_template("products_show.html", product=product)


@app.route("/about-us")
def about():
    return render_template("about.html")


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    product = conn.execute(
        'SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if product:
        image_filename = product['image_filename']
        if image_filename:
            image_path = Path(__file__).parent / 'static' / \
                'images' / 'products' / image_filename
            if image_path.exists():
                os.remove(image_path)

        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()

    conn.close()
    return redirect(url_for('products'))


if __name__ == "__main__":
    app.run(debug=True)
