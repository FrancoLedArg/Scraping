# Project Documentation

Quick disclaimer: for this project i learned python + scrapy in like a month, don't expect anything too complex (?

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)

## Introduction
This Book Scraper project is a web scraping project that I have developed as part of my portfolio. The project demonstrates my skills in web scraping, data extraction, and data storage. The primary goal of the project is to collect book data from https://books.toscrape.com/ and store it in a database. In the future, I plan to integrate GPT to enhance the data with more detailed information.

## Installation and Usage
To install this project, follow these steps:

1. Create a virtual environment to isolate project dependencies: `python -m venv venv`
2. Activate the virtual environment:
    - For Windows(cmd): `venv\Scripts\activate.bat`
    - For Windows(powershell): `venv\Scripts\Activate.ps1`
    - For macOS/Linux: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database:
    - This project works with a docker image, so make sure to have docker installed on your system.
    - Create a `.env` file with the structure given in the `.env.example` file to set up the database.
    - If you don't want to use a database, there is instructions in the `settings.py` and `pipelines.py`
    files to remove this functionality.
5. Run the docker container: `docker-compose --env-file .env up`
6. Run the Book Scraper:
    - Navigate to `./bookscraper/bookscraper`
    - Run the Spider: `scrapy crawl bookspider`
7. Access the data:
    - The Book Scraper will generate a json file in the `./bookscraper/bookscraper` directory,
    or you can access it through the database in the `localhost:8080` port via phpMyAdmin

## For learning porpuses i'm not removing the coments from the scrapy docs in the files
