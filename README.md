<div align="center">

# Vulnhub Scraper

<img src="image.png">

</div>

Vulnhub Scraper is a Python terminal application that lets you scrape data from machines on [vulnhub.com](https://vulnhub.com) that match a given term.

## Usage
```
Usage: python main.py [options]
    Options:
        -h, --help: Show this help message
        -f, --file: File to save the data
        -t, --term: Term to search
        -e, --extended: Optional. Save extended information.

Example:
    python3 main.py -f data.txt -t "Difficulty: Easy" -e
```