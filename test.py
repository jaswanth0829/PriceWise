import requests

from bs4 import BeautifulSoup

url = "https://www.amazon.in/dp/B0DXQH1DBS"

headers = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

response = requests.get(
    url,
    headers=headers
)

print("STATUS CODE:")
print(response.status_code)

soup = BeautifulSoup(
    response.text,
    "lxml"
)

title = soup.find(
    id="productTitle"
)

price = soup.find(
    "span",
    class_="a-price-whole"
)

print("\nTITLE:\n")
print(title)

print("\nPRICE:\n")
print(price)