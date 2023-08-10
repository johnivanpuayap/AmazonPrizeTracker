import os
from bs4 import BeautifulSoup
import requests
import lxml
import smtplib

MY_EMAIL = "johnivanpuayapamerica@gmail.com"
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

print("Welcome to Amazon Price Tracker!\n")
url = input("Please enter the URL that you want to keep track of: ")
budget = float(input("Please enter your budget (in $): "))
user_email = input("Please enter your email: ")

# Connect to the URL
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
                                                    "KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                                      "Accept-Language": "en-US,en;q=0.6"})

soup = BeautifulSoup(response.text, 'lxml')

# Find the Price
price_container = soup.find(name="span", class_="a-price a-text-price a-size-medium apexPriceToPay")
if price_container is not None:
    price = float(price_container.findChildren()[1].text.split('$')[1])
    print(price)
else:
    print("Price not found. Exiting..")
    exit()

# Find the Title
title_container = soup.find(name="span", id="productTitle")
title = title_container.text.strip()
print(title)

# Check if price is within budget to send the mail
if price <= budget:
    message = message = f"Subject: Amazon Price Alert!\n\n{title} is now at ${price}\n Buy it here now: {url}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=user_email, msg=message)
        