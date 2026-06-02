import sqlite3
import requests
from bs4 import BeautifulSoup
import schedule
import time

def update_prices():

    print("Checking prices...")

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    # Get all products
    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    for product in products:

        product_id = product[0]

        old_price = float(product[2])

        product_url = product[3]

        try:

            response = requests.get(product_url)

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            new_price = soup.find(
                "p",
                class_="price_color"
            ).text

            new_price = new_price.replace("£", "")

            new_price = float(new_price)

            # If price changed
            if new_price != old_price:

                print("Price changed!")

                # Update products table
                cursor.execute(
                    """
                    UPDATE products

                    SET price=?

                    WHERE id=?
                    """,
                    (
                        new_price,
                        product_id
                    )
                )

                # Add history entry
                cursor.execute(
                    """
                    INSERT INTO price_history
                    (product_id, price)

                    VALUES (?, ?)
                    """,
                    (
                        product_id,
                        new_price
                    )
                )

                conn.commit()

                print(
                    f"Updated: {old_price} → {new_price}"
                )

        except Exception as e:

            print("Error:", e)

    conn.close()

# Run every 1 minute
schedule.every(1).minutes.do(update_prices)

print("Auto updater running...")

while True:

    schedule.run_pending()

    time.sleep(1)