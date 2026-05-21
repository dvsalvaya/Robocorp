import http

from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF

@task
def robot():
    """Insert the sales data for the week and export it as a PDF"""
    browser.configure(
        slowmo=1500,
    )
    open_web()
    log_in()
    get_orders()

def open_web():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    page = browser.page()
    page.click("text=ok")



def get_orders():
    """get csv file from the given URL"""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)
    library = Tables()

    orders = library.read_table_from_csv("orders.csv")

    for order in orders:
        insert_data(order)
    

def insert_data(order):
    """Fills in the sales data and click the 'Submit' button"""

    page = browser.page()

    page.select_option("#head", order["Head"])

    page.check(f'input[value="{order["Body"]}"]')

    page.get_by_label("3. Legs:").fill(str(order["Legs"]))

    page.fill("#address", order["Address"])

    page.click("text=Order")

def store_receipt_as_pdf(order_number):
    """Take a screenshot of the page and save it as a PDF"""
    page = browser.page()
    pdf = PDF()
    pdf.create_pdf_from_page(page, f"receipt_{order_number}.pdf")