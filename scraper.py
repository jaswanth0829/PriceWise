import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Download webpage
response = requests.get(url)

# Convert HTML into readable object
soup = BeautifulSoup(response.text, "html.parser")

# Find product title
title = soup.find("h1").text

# Find product price
price = soup.find("p", class_="price_color").text

print("Product:", title)
print("Price:", price)