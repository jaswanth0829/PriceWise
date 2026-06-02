from flask import Flask, render_template, request, redirect
import sqlite3
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        product_url = request.form.get("url")

        target_price = request.form.get("target_price")

        if product_url:

            response = requests.get(product_url)

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            product_name = soup.find("h1").text

            product_price = soup.find(
                "p",
                class_="price_color"
            ).text

            product_price = product_price.replace("£", "")

            cursor.execute(
                """
                INSERT INTO products
                (name, price, url, target_price)

                VALUES (?, ?, ?, ?)
                """,
                (
                    product_name,
                    product_price,
                    product_url,
                    target_price
                )
            )

            conn.commit()

            product_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO price_history
                (product_id, price)

                VALUES (?, ?)
                """,
                (
                    product_id,
                    product_price
                )
            )

            conn.commit()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    cursor.execute("""
    SELECT
        products.name,
        price_history.price,
        price_history.date

    FROM price_history

    JOIN products
    ON products.id = price_history.product_id
    """)

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        products=products,
        history=history
    )

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)