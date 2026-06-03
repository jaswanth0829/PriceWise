import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import schedule
import time

from db import get_connection

from services.scraper import (
    scrape_product
)

from services.email_service import (
    send_price_alert
)

from app import app

from config import UPDATE_INTERVAL

def update_prices():

    print(
        "Checking prices..."
    )

    conn = get_connection()

    cursor = conn.cursor()

    # GET PRODUCTS + USER EMAIL
    cursor.execute(
        """
        SELECT
            products.id,
            products.name,
            products.price,
            products.url,
            products.target_price,
            users.email

        FROM products

        INNER JOIN users
        ON products.user_id = users.id
        """
    )

    products = cursor.fetchall()

    for product in products:

        product_id = product[0]

        product_name = product[1]

        old_price = float(product[2])

        product_url = product[3]

        target_price = float(product[4])

        user_email = product[5]

        print(
            f"""
            Product:
            {product_name}

            Alert Email:
            {user_email}
            """
        )

        try:

            scraped_product = (
                scrape_product(
                    product_url
                )
            )

            if scraped_product:

                new_price = float(
                    scraped_product["price"]
                )

                # UPDATE PRICE
                if new_price != old_price:

                    print(
                        f"""
                        Price updated:
                        {old_price}
                        →
                        {new_price}
                        """
                    )

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

                    cursor.execute(
                        """
                        INSERT INTO
                        price_history

                        (
                            product_id,
                            price
                        )

                        VALUES (?, ?)
                        """,
                        (
                            product_id,
                            new_price
                        )
                    )

                    conn.commit()

                # EMAIL ALERT
                if new_price <= target_price:

                    print(
                        f"""
                        Sending alert to:
                        {user_email}
                        """
                    )

                    send_price_alert(
                        app,
                        user_email,
                        product_name,
                        new_price
                    )

        except Exception as e:

            print(
                "Updater Error:",
                e
            )

    conn.close()

schedule.every(
    UPDATE_INTERVAL
).minutes.do(
    update_prices
)

print(
    "Auto updater running..."
)

while True:

    schedule.run_pending()

    time.sleep(1)