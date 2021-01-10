import requests
from bs4 import BeautifulSoup

url = "https://www.vulnhub.com/"

# Check if site is up
def checkSite(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
        return False
    except:
        return False

# Get Page
def getPage(url):
    r = requests.get(url)
    return r

# Get number of pages
def getNumberPages(url):
    # If we request a large number like 100 we get the last page
    # and with that, we can get the total number.
    url = url
    page = getPage(url + "/?page=100")
    soup = BeautifulSoup(page.content, 'html.parser')

    number = int(soup.find("a", {"class": "page-link"})["href"][-2:]) + 1
    return number



# Get list of machines in a certain page

# Get description of machine


def main():
    if not checkSite(url):
        print("No se puede aceder al sitio.")
        exit()
    term = input("Term to search: ")
    print("Searching:", term)
    number_pages = getNumberPages(url)
    for i in range(1, number_pages + 1):
        print(i)
        

if __name__ == "__main__":
    main()