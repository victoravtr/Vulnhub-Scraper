import requests
from bs4 import BeautifulSoup

url = "https://www.vulnhub.com"

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
    page = getPage(url + "/?page=100")
    soup = BeautifulSoup(page.content, 'html.parser')
    number = int(soup.find("a", {"class": "page-link"})["href"][-2:]) + 1
    return number


# Get list of machines in a certain page
def getMachines(url):
    page = getPage(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    machines = soup.findAll("div", {"class": "card-title"})
    machineList = []
    for machine in machines:
        machineList.append("https://www.vulnhub.com" + machine.find("a")["href"])
    return machineList

# Get description of machine
def getDescription(url):
    page = getPage(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    machines = soup.find("div", {"id": "description"}).text
    print(machines)

def main():
    if not checkSite(url):
        print("Error while trying to access vulnhub.")
        exit()
    term = input("Term to search: ")
    if term == "":
        print("You need to set a search term")
        exit()
    print("Searching:", term)
    number_pages = getNumberPages(url)
    for i in range(1, number_pages + 1):
        machineList = getMachines(url + "?page=" + str(i))
        for machine in machineList:
            description = getDescription(machine)
            if term in description:
                


if __name__ == "__main__":
    main()