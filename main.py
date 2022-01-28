""" Python utility to scrape data from vulnhub.com """
import inspect
import re
import sys
import urllib.parse
import os
from bs4 import BeautifulSoup
from colorama import init, Fore
import requests


def check_site(url):
    """ Check if vulnhub.com is working

    Args:
        url (str): URL to check

    Returns:
        bool: True if vulnhub.com is working, False otherwise
        Also:
            if bool is True: returns code status as int
            if bool is False: returns HTTPError object
    """
    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return True, response.status_code
        if response.status_code == requests.codes.bad:
            return False, response.raise_for_status()
        return response.raise_for_status()
    except Exception:
        print(exception_info(sys.exc_info()))
        sys.exit(1)


def get_soup(url):
    """ Get BeautifulSoup object from a URL

    Args:
        url (str): URL to get the BeautifulSoup object from

    Returns:
        bs4_obj (bs4.BeautifulSoup): BeautifulSoup object
    """
    try:
        page_content = requests.get(url)
        soup = BeautifulSoup(page_content.content, 'html.parser')
        return soup
    except Exception:
        print(exception_info(sys.exc_info()))
        sys.exit(1)


def get_number_machines(url):
    """ Get number of machines in a certain page

    Args:
        url (str): URL to get the number of machines from

    Returns:
        int: Number of machines in a certain page
    """
    soup = get_soup(url)
    try:
        titles = soup.find_all('h2')
        for title in titles:
            if title.text.startswith("Search Result"):
                return int(re.findall("\\d+", title.text)[0])
            raise Exception
    except Exception:
        print(exception_info(sys.exc_info()))
        sys.exit(1)


def get_machine_urls(url):
    """ Get all machine links from a given url

    Args:
        url (str): URL to get the machine links from

    Returns:
        list: List of machines links
    """
    soup = get_soup(url)
    machine_list = []
    for machine in soup.findAll('div', {'class': 'card-title'}):
        machine_list.append(
            f"https://www.vulnhub.com{machine.find('a')['href']}")
    return machine_list


def get_basic_info(soup):
    """ Get basic machine information

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoup object

    Returns:
        dict: Dictionary with basic machine information
    """
    title = soup.find("meta", {'property': 'og:title'})
    url = soup.find("meta", {'property': 'og:url'})
    return {
        'title': title['content'],
        'url': url['content']
    }


def get_about_release(soup):
    """ Get about release information

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoup object

    Returns:
        str: About release information
    """
    try:
        about_release = soup.find('div', {'id': 'release'})
        return remove_junk(about_release)
    except Exception:
        print(exception_info(sys.exc_info()))
        sys.exit(1)


def get_description(soup):
    """ Get description information

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoup object

    Returns:
        str: Description information
    """
    try:
        description = soup.find('div', {'id': 'description'})
        return remove_junk(description)
    except Exception:
        print(exception_info(sys.exc_info()))
        sys.exit(1)


def remove_junk(bs4_obj):
    """ Remove things we don't want from a BeautifulSoup object and returns it as a string

    Args:
        bs4_obj (bs4.BeautifulSoup): BeautifulSoup object

    Returns:
        str: String without things we don't want
    """
    banned_tags = ['About Release', 'Description', 'Back to the Top']
    if bs4_obj.find('div', {'class': 'modal'}):
        bs4_obj.find('div', {'class': 'modal'}).decompose()
    if bs4_obj.find('a', {'href': '#top'}):
        bs4_obj.find('a', {'href': '#top'}).decompose()
    text_list = list(filter(None, bs4_obj.text.split('\n')))
    line_number = 0
    for line in text_list:
        line = line.strip()
        if line in banned_tags:
            del text_list[line_number]
        line_number += 1
    # convert list to string
    return '\n'.join(text_list)


def save_to_file(filename, content):
    """ Save data to a file

    Args:
        filename (str): File to save the data
        content (str): Data to save
    """
    with open(filename, 'a+', encoding='utf8') as writer:
        writer.write(content)


def get_machine_data(soup, flag):
    """ Get machine data

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoup object with the machine page info
        flag (bool): If True, save extended information

    Returns:
        str: Machine data
    """
    basic_info = get_basic_info(soup)
    data_string = "---------- Machine ----------\n"
    data_string += f"Title: {basic_info['title']}\n"
    data_string += f"URL: {basic_info['url']}\n"

    if flag:
        data_string += "---------- Description ----------\n" + \
            get_description(soup) + '\n'
        data_string += "---------- About Release ----------\n" + \
            get_about_release(soup) + '\n'
    data_string += "\n"
    return data_string


def help_menu():
    """ Help menu

    Returns:
        str: Help menu
    """
    return """
            Usage: python main.py [options]
                Options:
                    -h, --help: Show this help message
                    -f, --file: File to save the data
                    -t, --term: Term to search
                    -e, --extended: Optional. Save extended information.
            """


def exception_info(sys_info):
    """ Returns a string with the exception information.
    Args:
        sys_info (tuple): sys.exc_info()
    Returns:
        str: exception information
    """
    exc_type, exc_value, exc_traceback = sys_info

    exception_name = exc_type.__name__
    file_source = os.path.split(exc_traceback.tb_frame.f_code.co_filename)[1]
    line_number = exc_traceback.tb_lineno
    function_name = exc_traceback.tb_frame.f_code.co_name
    value = exc_value

    return f"{exception_name} while executing {file_source}:{function_name}:{line_number}: {value}"


if __name__ == "__main__":
    init(wrap=True, autoreset=True)

    if len(sys.argv[1:]) == 0:
        print(f"{Fore.RED}[!] No arguments given.")
        print(inspect.cleandoc(help_menu()))
        sys.exit(0)

    arguments = sys.argv[1:]
    if '-h' in arguments or '--help' in arguments:
        print(inspect.cleandoc(help_menu()))
        sys.exit(0)

    if '-f' not in arguments and '--file' not in arguments:
        print(f"{Fore.RED}[!] No file given.")
        print(inspect.cleandoc(help_menu()))
        sys.exit(0)
    if '-f' in arguments:
        file_path = arguments[arguments.index('-f') + 1]
    else:
        file_path = arguments[arguments.index('--file') + 1]

    if '-t' not in arguments and '--term' not in arguments:
        print(f"{Fore.RED}[!] No term given.")
        print(inspect.cleandoc(help_menu()))
        sys.exit(0)
    if '-t' in arguments:
        term = arguments[arguments.index('-t') + 1]
    else:
        term = arguments[arguments.index('--term') + 1]

    EXTENDED = '-e' in arguments or '--extended' in arguments

    BASE_URL = "https://www.vulnhub.com"
    status, code = check_site(BASE_URL)
    if not status:
        print(f"{Fore.RED}Status code: {code}")
        print(f"{Fore.RED}Site is down")
        sys.exit(0)
    print(f"{Fore.GREEN}Status code: {code}")
    print(f"{Fore.GREEN}Site is up!")

    print(f"Searching: {term}\n")

    ENCODED_TERM = urllib.parse.urlencode({'q': term})
    NUMBER_MACHINES = get_number_machines(f"{BASE_URL}/?{ENCODED_TERM}")
    print(f"Machines: {NUMBER_MACHINES}")
    if NUMBER_MACHINES == 0:
        print("No machines found for the given term.")
        print(f"\n{Fore.GREEN}Done!")
        sys.exit(0)

    SLOT_NUMBER = 10
    page = 1
    index = 1
    remaining_machines = NUMBER_MACHINES
    while remaining_machines > 0:
        page_url = f"{BASE_URL}/?page={page}&{ENCODED_TERM}"
        machines_url = get_machine_urls(page_url)

        for machine_url in machines_url:
            machine_data = get_machine_data(get_soup(machine_url), EXTENDED)
            save_to_file(file_path, machine_data)
            percentage = round(index / NUMBER_MACHINES * 100, 1)
            filled = int(index / NUMBER_MACHINES * SLOT_NUMBER)
            fill_string = f"{'#' * filled}{' ' * (SLOT_NUMBER - filled)}"
            print(
                f"Progress: {percentage}% [{fill_string}] {index}/{NUMBER_MACHINES}", end='\r')
            index += 1
            remaining_machines -= 1
        page += 1
    print(f"\n{Fore.GREEN}Done!")
