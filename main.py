import os
import time
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
                                      "Accept-Language": "en-US,en;q=0.6",
                                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                                                "image/webp,image/apng,*/*;q=0.8",
                                      "referer": "https://www.amazon.com/"})

soup = BeautifulSoup(response.text, 'lxml')


def find():
    print(soup)
    if soup.find(name="p", class_="a-last"):
        print("Captcha HTML was returned. Trying again!")
        time.sleep(10)
        find()
    else:
        find_price_and_title()


def find_price_and_title():
    # Find the Price
    print("Finding the Price")
    price_container = soup.find(name="span", class_="a-price a-text-price a-size-medium apexPriceToPay")
    if price_container is None:
        price_container = soup.find(name="span", class_="aok-offscreen")
        if price_container is None:
            print("Price couldn't be found. Please use another link.")
            exit()
        else:
            price = float(price_container.text.split('$')[1])
            print(price)
    else:
        price = float(price_container.findChildren()[1].text.split('$')[1])
        print(price)

    # Find the Title
    print("Finding the Title")
    title_container = soup.find(name="span", id="productTitle")
    title = title_container.text.strip()
    print(title)

    send_email(title, price)


def send_email(title, price):
    print("Sending an Email")
    # Check if price is within budget to send the mail
    if price <= budget:
        message = message = f"Subject: Amazon Price Alert!\n\n{title} is now at ${price}\n Buy it here now: {url}"
        print(message)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=user_email, msg=message)


find()
