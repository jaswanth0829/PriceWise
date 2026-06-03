from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_mail import Mail

from config import *

from db import get_connection

from services.scraper import scrape_product

from services.email_service import (
    mail
)

app = Flask(__name__)

app.secret_key = "pricewise_secret"

# MAIL CONFIG
app.config["MAIL_SERVER"] = MAIL_SERVER

app.config["MAIL_PORT"] = MAIL_PORT

app.config["MAIL_USE_TLS"] = MAIL_USE_TLS

app.config["MAIL_USERNAME"] = MAIL_USERNAME

app.config["MAIL_PASSWORD"] = MAIL_PASSWORD

mail.init_app(app)

# HOME
@app.route("/", methods=["GET", "POST"])
def home():

    if "user_id" not in session:

        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor()

    user_id = session["user_id"]

    if request.method == "POST":

        product_url = request.form.get(
            "url"
        )

        target_price = request.form.get(
            "target_price"
        )

        product = scrape_product(
            product_url
        )

        if product:

            cursor.execute(
                """
                INSERT INTO products
                (
                    user_id,
                    name,
                    price,
                    url,
                    target_price
                )

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    product["name"],
                    product["price"],
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
                    product["price"]
                )
            )

            conn.commit()

    cursor.execute(
        """
        SELECT * FROM products
        WHERE user_id=?
        """,
        (user_id,)
    )

    products = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            products.name,
            price_history.price,
            price_history.date

        FROM price_history

        JOIN products
        ON products.id =
        price_history.product_id

        WHERE products.user_id=?
        """,
        (user_id,)
    )

    history = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        products=products,
        history=history
    )

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        hashed_password = (
            generate_password_hash(
                password
            )
        )

        conn = get_connection()

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    email,
                    password
                )

                VALUES (?, ?, ?)
                """,
                (
                    username,
                    email,
                    hashed_password
                )
            )

            conn.commit()

            conn.close()

            return redirect("/login")

        except Exception as e:

            return f"""
            Registration Error:
            {e}
            """

    return render_template(
        "register.html"
    )

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=?
            """,
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(
            user[3],
            password
        ):

            session["user_id"] = user[0]

            return redirect("/")

        else:

            return "Invalid username or password."

    return render_template(
        "login.html"
    )

# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# API
@app.route("/api/products")
def api_products():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    conn.close()

    product_list = []

    for product in products:

        product_data = {
            "id": product[0],
            "name": product[2],
            "price": product[3],
            "url": product[4],
            "target_price": product[5]
        }

        product_list.append(
            product_data
        )

    return jsonify(product_list)

# DELETE
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE id=?
        """,
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect("/")

if __name__ == "__main__":

    app.run(debug=True)