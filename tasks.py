from robocorp.tasks import task
from robocorp import browser

from RPA.Tables import Tables
from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Archive import Archive

@task
def init():
    # browser.configure(slowmo=1000)
    # open_browser()
    # dowload_csv()
    # get_oders()
    archive_receipts()


def open_browser():
    """Abre o navegador e acessa a página de pedidos de robôs."""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def log_in():
    page = browser.page()
    page.click("button:text('OK')")

def dowload_csv():
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv")

def get_oders():
    lib = Tables()
    orders = lib.read_table_from_csv("orders.csv", columns=["Order number","Head","Body","Legs","Address"])
    for order in orders:
        log_in()
        preencher(order)
        log_out()


def preencher(order):

    page = browser.page()
    page.select_option("#head", order['Head'])
    page.check(f"input[value='{order['Body']}']")
    page.get_by_placeholder("Enter the part number for the legs").fill(order['Legs'])
    page.fill("#address",str(order['Address']))
    page.click("button:text('ORDER')")

    pdf = PDF()
    sales_results_html = page.locator("#order-completion").inner_html()
    pdf.html_to_pdf(sales_results_html,f"recipts/order_{order['Order number']}.pdf")
    
    page.screenshot(path=f"recipts/robo_{order['Order number']}.png")


def log_out():
    page = browser.page()
    page.click("button:text('ORDER ANOTHER ROBOT')")

def get_pdf():
    page = browser.page()
    
def archive_receipts():
    lib = Archive()

    lib.archive_folder_with_zip(
        folder="recipts/",
        archive_name="recipts.zip"
    )