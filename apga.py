import requests

csv_data = requests.get("https://robotsparebinindustries.com/orders.csv")

for order in csv_data:
    print(order)