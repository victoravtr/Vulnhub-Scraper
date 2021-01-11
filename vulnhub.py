import requests
import re
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
    page = getPage(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    number = soup.find("a", {"class": "page-link"})["href"]
    return re.findall('\d+', number)



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
    return soup.find("div", {"id": "description"}).text
    

def main():
    if not checkSite(url):
        print("Error while trying to access vulnhub.")
        exit()
    term = input("Term to search: ")
    if term == "":
        print("You need to set a search term")
        exit()
    print("Searching:", term)
    
    # Hacemos una busqueda inicial
    # Con esa busqueda optenemos el numero total de paginas
    number_pages = getNumberPages(url + "/?page=110&q=" + term)
    print(number_pages)
    # De cada pagina cogemos la lista de maquinas
    # Por cada maquina buscamos descripcion y url y lo guardamos en un archivo


if __name__ == "__main__":
    main()