from bs4 import BeautifulSoup
from colorama import init, Fore
import requests
import re


init(wrap=True, autoreset=True)
url = "https://www.vulnhub.com"


def check_site(url):  # Check if site is up
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
        return False
    except Exception as ex:
        return False


def get_page(url):  # Get Page
    r = requests.get(url)
    return r


def get_number_pages(url):  # Get number of pages
    # If we request a large number like 100 we get the last page
    # and with that, we can get the total number.
    page = get_page(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        number = soup.find("a", {"class": "page-link"})["href"]
        print(number)
        return int(re.findall('\d+', number)[0]) + 1
    except Exception as ex:
        return 0


def get_machines(url):  # Get list of machines in a certain page
    page = get_page(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    machines = soup.findAll("div", {"class": "card-title"})
    machineList = []
    for machine in machines:
        machineList.append("https://www.vulnhub.com" +
                           machine.find("a")["href"])
    return machineList


def get_description(url):  # Get description of machine
    page = get_page(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        p_list = soup.find("div", {"id": "description"}).text
        p_list = remove_junk(p_list)
    except Exception as exc:
        p_list = ""
    return p_list


def remove_junk(text):
    index = 0
    text = text.split('\n')
    text = list(filter(None, text))
    for line in text:
        line = line.strip()
        if line == ' ':
            del text[index]
        if line == '':
            del text[index]
        if line == 'Back to the Top':
            del text[index]
        index += 1
    return text


def save_to_file(file_name, machines):
    with open(file_name, 'w') as file:
        for machine in machines:
            description = get_description(machine)
            file.write("URL: " + machine + '\n')
            for line in description:
                file.write(" | " + line + '\n')
            file.write('\n')
            file.write("-------------------------" + '\n')
            file.write('\n')


def main():
    if not check_site(url):
        print(Fore.RED + "Site is down")
        exit()
    print(Fore.GREEN + "Site is up!")

    term = input("Term to search: ")
    if term == "":
        print(Fore.RED + "You need to set a search term")
        exit()
    print("Searching:", term)

    # If we search for a large number, we can get the last page for that term
    number_pages = get_number_pages(url + "/?page=1000&q=" + term)
    if number_pages == 0:
        print(Fore.RED + str(number_pages) + " pages found")
        exit(0)
    print(Fore.GREEN + str(number_pages) + " pages found")

    # For each page get a list of machines
    for i in range(1, int(number_pages) + 1):
        base_url = url + "/?page=" + str(i) + "&q=" + term
        print("Getting machines from: " + base_url)
        machines = get_machines(base_url)
        # For each machine we save url and description into 'file'
        file_name = term + "_" + str(i)
        save_to_file(file_name, machines)


if __name__ == "__main__":
    main()
