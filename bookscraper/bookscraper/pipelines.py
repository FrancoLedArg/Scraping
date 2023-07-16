# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Personal imports
import re

# For enviroment variables
import os
from dotenv import load_dotenv

# For MySQL
from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class BookscraperPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        for field_name in field_names:
            if field_name != "description" and field_name != "product_info":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
            
            if field_name == "description":
                text = adapter.get(field_name)
                clean_text = re.sub(r'[^\x00-\x7F]+', '', text)
                adapter["description"] = clean_text

            if field_name == "rating":
                possible_ratings = {
                    "One": 1,
                    "Two": 2,
                    "Three": 3,
                    "Four": 4,
                    "Five": 5
                }

                if adapter["rating"].startswith("star-rating"):
                    words = adapter["rating"].split()[1:]
                    stars = possible_ratings.get(" ".join(words))
                    if stars:
                        adapter["rating"] = stars

            if field_name == "product_info":
                availability = adapter["product_info"].get("availability")
                available = availability.split('(')[1].split()[0]
                adapter["product_info"]["availability"] = int(available)

                num_reviews = adapter["product_info"].get("number_of_reviews")
                adapter["product_info"]["number_of_reviews"] = int(num_reviews)

        return item

# Remove the following pipeline if you do not want to use a database

# Load environment variables from .env file
load_dotenv('../../.env')

# Define the SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")

# You could use the following structure if the string above lacks readability

'''
engine = create_engine(
    "mysql+mysqlconnector://"
    + os.getenv('MYSQL_USER')+ ":"
    + os.getenv('MYSQL_PASSWORD') + "@"
    + os.getenv('MYSQL_HOST') + ':'
    + os.getenv('MYSQL_PORT') + '/'
    + os.getenv('MYSQL_DATABASE')
)
'''


# Create a Session class for database sessions
Session = sessionmaker(bind = engine)

# Create a base class for declarative models
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(String(20))
    rating = Column(Integer)
    category = Column(String(255))
    description = Column(Text)
    product_type = Column(String(255))
    price_excl_tax = Column(String(20))
    price_incl_tax = Column(String(20))
    tax = Column(String(20))
    availability = Column(Integer)
    number_of_reviews = Column(Integer)

class SaveToMySQLPipeline:

    def __init__(self):
        self.session = Session()
        
        # Create tables if they don't exist
        Base.metadata.create_all(engine)

    def process_item(self, item, spider):
        book = Book(
            name=item["name"],
            price=item["price"],
            rating=item["rating"],
            category=item["category"],
            description=item["description"],
            product_type=item["product_info"]["product_type"],
            price_excl_tax=item["product_info"]["price_excl_tax"],
            price_incl_tax=item["product_info"]["price_incl_tax"],
            tax=item["product_info"]["tax"],
            availability=item["product_info"]["availability"],
            number_of_reviews=item["product_info"]["number_of_reviews"]
        )

        self.session.add(book)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
