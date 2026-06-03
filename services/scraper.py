import requests

from bs4 import BeautifulSoup

def scrape_product(url):

    headers = {

        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),

        "Accept-Language":
        "en-US,en;q=0.9"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print(
            "STATUS CODE:",
            response.status_code
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        # =========================
        # AMAZON
        # =========================

        if "amazon" in url:

            title = soup.find(
                id="productTitle"
            )

            price = soup.select_one(
                "span.a-price span.a-offscreen"
            )

            print(
                "Amazon title:",
                title
            )

            print(
                "Amazon price:",
                price
            )

            if title and price:

                product_name = (
                    title.text.strip()
                )

                product_price = (
                    price.text
                    .replace("₹", "")
                    .replace(",", "")
                    .strip()
                )

                return {
                    "name": product_name,
                    "price": float(product_price)
                }

        # =========================
        # FLIPKART
        # =========================

        elif "flipkart" in url:

            title = soup.find(
                "span",
                class_="VU-ZEz"
            )

            price = soup.find(
                "div",
                class_="Nx9bqj CxhGGd"
            )

            print(
                "Flipkart title:",
                title
            )

            print(
                "Flipkart price:",
                price
            )

            if title and price:

                product_name = (
                    title.text.strip()
                )

                product_price = (
                    price.text
                    .replace("₹", "")
                    .replace(",", "")
                    .strip()
                )

                return {
                    "name": product_name,
                    "price": float(product_price)
                }

        # =========================
        # MYNTRA
        # =========================

        elif "myntra" in url:

            title = soup.find(
                "h1",
                class_="pdp-title"
            )

            brand = soup.find(
                "h1",
                class_="pdp-name"
            )

            price = soup.find(
                "span",
                class_="pdp-price"
            )

            print(
                "Myntra title:",
                title
            )

            print(
                "Myntra brand:",
                brand
            )

            print(
                "Myntra price:",
                price
            )

            if title and brand and price:

                product_name = (
                    brand.text.strip()
                    + " "
                    + title.text.strip()
                )

                product_price = (
                    price.text
                    .replace("Rs. ", "")
                    .replace(",", "")
                    .strip()
                )

                return {
                    "name": product_name,
                    "price": float(product_price)
                }

        # =========================
        # BOOKSTOSCRAPE
        # =========================

        else:

            title = soup.find("h1")

            price = soup.find(
                "p",
                class_="price_color"
            )

            print(
                "Book title:",
                title
            )

            print(
                "Book price:",
                price
            )

            if title and price:

                product_name = (
                    title.text.strip()
                )

                product_price = (
                    price.text
                    .replace("£", "")
                    .replace("Â", "")
                    .strip()
                )

                return {
                    "name": product_name,
                    "price": float(product_price)
                }

        print(
            "Could not scrape product."
        )

        return None

    except Exception as e:

        print(
            "Scraper Error:",
            e
        )

        return None