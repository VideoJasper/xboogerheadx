import sqlite3
from pathlib import Path
from flask import Flask, render_template


app = Flask(__name__)


def get_db_connection():
    """
    Izveido un atgriež savienojumu ar SQLite datubāzi.
    """
    # Atrod ceļu uz datubāzes failu (tas atrodas tajā pašā mapē, kur šis fails)
    db = Path(__file__).parent / "Cepumkaste.db"
    # Izveido savienojumu ar SQLite datubāzi
    conn = sqlite3.connect(db)
    # Nodrošina, ka rezultāti būs pieejami kā vārdnīcas (piemēram: product["name"])
    conn.row_factory = sqlite3.Row
    # Atgriež savienojumu
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/produkti")
def products():
    conn = get_db_connection()  # Pieslēdzas datubāzei

    # Izpilda SQL vaicājumu, kas atlasa visus produktus
    products = conn.execute("SELECT * FROM products").fetchall()

    conn.close()  # Aizver savienojumu ar datubāzi

    # Atgriežam HTML veidni "products.html", padodot produktus veidnei
    return render_template("products.html", products=products)
    # return render_template("products.html")

# Maršruts, kas atbild uz pieprasījumu, piemēram: /produkti/3
# Šeit <int:product_id > nozīmē, ka URL daļā gaidāms produkta ID kā skaitlis
@app .route ("/ <int:product_id>")
def products_show(product_id):
    conn = get_db_connection () # Pieslēdzas datubāzei

    # Izpilda SQL vaicājumu, kurš atgriež tikai vienu produktu pēc ID
    product = conn.execute(
        """
        SELECT "products".*, "producers"."name" AS "producer"
        FROM products
        LEFT JOIN "producers" ON "products"."producer_id" = "producers"."id"
        WHERE "products"."id" = ?
        """,
        (product_id,),
    ).fetchone()
    # ? ir vieta, kur tiks ievietota vērtība - šajā gadījumā product_id
    conn. close () # Aizver savienojumu ar datubāzi

    # Atgriežam HTML veidni 'products_show.html', padodot konkrēto produktu veidnei
    return render_template ("products_show.html", product=product)


@app.route("/par-mums")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
