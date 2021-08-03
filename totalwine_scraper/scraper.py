import os
import pandas as pd
import requests
import time
import numpy as np
import json
import math
from typing import Set
from json.decoder import JSONDecodeError
from typing import Dict, Any, Union


class Scraper:

    def __init__(self, number_of_items: int, item_types: list) -> None:
        """
        This scrapes totalwine.com for wine listings
        It is able to take demanded number of listings and a list of different types of wines to scrape.
        Returns a dataframe or csv file with tabular data.

        Args:
            number_of_items (int): demanded number of listings
            item_types (list): list of preferred wine types
        """

        self.__number_of_items = number_of_items
        self.__item_types = ["".join(item.split()).title() for item in item_types]
        self.items_per_page = 200

    @property
    def number_of_items(self) -> int:
        return self.__number_of_items

    @property
    def item_types(self) -> list:
        return self.__item_types

    @property
    def number_of_pages(self) -> int:
        return math.ceil(self.__number_of_items / self.items_per_page)

    @property
    def items_to_return(self) -> int:
        return len(self.__item_types) * self.__number_of_items

    @staticmethod
    def get_headers(page: int, wine_type: str) -> dict:
        headers = {
            "authority": "www.totalwine.com",
            "sec-ch-ua": "^\\^",
            "accept": "application/json, text/plain, */*",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": f"https://www.totalwine.com/wine/c/c0020?&page={(page - 1)}&pageSize=200&department=Wine&producttype={wine_type}^%^20Wine&aty=1,1,0,1",
            "accept-language": "en-US,en;q=0.9",
        }
        return headers

    @staticmethod
    def get_params(page: int, wine_type: str) -> Set:
        params = (
            ("page", f"{page}"),
            ("pageSize", "200"),
            ("state", "US-CA"),
            ("shoppingMethod", "INSTORE_PICKUP^%^2CDELIVERY"),
            ("userShoppingMethod", "INSTORE_PICKUP"),
            ("allStoresCount", "true"),
            ("searchAllStores", "true"),
            ("storeId", "1108"),
            ("department", "Wine"),
            ("producttype", f"{wine_type}^%^20Wine"),
        )
        return params

    def get_response(
        self, page: int, wine_type: str
    ) -> Union[requests.models.Response, str]:
        try:
            response = requests.get(
                f"https://www.totalwine.com/search/api/product/categories/v2/categories/c0020/products?page={page}&pageSize=200&state=US-CA&shoppingMethod=INSTORE_PICKUP%2CDELIVERY&userShoppingMethod=INSTORE_PICKUP&allStoresCount=true&searchAllStores=true&storeId=1108&department=Wine&producttype={wine_type}%20Wine",
                headers=self.get_headers(page, wine_type),
                params=self.get_params(page, wine_type),
            )
            response.raise_for_status()

            if response.status_code == 200:
                return response

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)

    def get_json(self, page: int, wine_type: str) -> Dict[str, Any]:
        """
        Returns json formatted variable for each page and wine type.
        """
        try:
            parsed = json.loads(self.get_response(page, wine_type).content)
            return parsed
        except JSONDecodeError as e:
            print(e)
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)

    def get_products(self, page: int, wine_type: str) -> Dict[str, Any]:
        """
        Checks if json file contains 200 items/page for each wine type and returns those products.
        """
        try:
            products = self.get_json(page, wine_type)["products"]
            if len(products) == 200:
                return products
        except:
            print("Corrupted json!")

    @staticmethod
    def get_brand(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            brand = item[id]["brand"]["name"]
        except:
            brand = None
        return brand

    @staticmethod
    def get_star_average(item: Dict[str, Any], id: int) -> Union[float, None]:
        try:
            stars = item[id]["customerAverageRating"]
        except:
            stars = None
        return stars

    @staticmethod
    def get_review_count(item: Dict[str, Any], id: int) -> Union[int, None]:
        try:
            review_count = item[id]["customerReviewsCount"]
        except:
            review_count = None
        return review_count

    @staticmethod
    def get_title(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            title = item[id]["name"]
        except:
            title = None
        return title

    @staticmethod
    def get_production_year(item: Dict[str, Any], id: int) -> Union[float, None]:
        try:
            extract_year = item[id]["name"].split(", ")[1]
            year = int(extract_year)
        except:
            year = None
        return year

    @staticmethod
    def get_rating_score(item: Dict[str, Any], id: int) -> Union[int, None]:
        try:
            rating = item[id]["rating"]
        except:
            rating = None
        return rating

    @staticmethod
    def get_description(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            description = item[id]["review"]
        except:
            description = None
        return description

    @staticmethod
    def is_winery_direct(item: Dict[str, Any], id: int) -> Union[int, None]:
        try:
            winery_direct = item[id]["directType"]
            if winery_direct == "Winery Direct":
                winery = 1
            else:
                winery = 0
        except:
            winery = 0
        return winery

    @staticmethod
    def get_img_link(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            img = item[id]["images"][0]["url"]
        except:
            img = None
        return img

    @staticmethod
    def get_item_link(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            link = "https://www.totalwine.com" + item[id]["productUrl"]
        except:
            link = None
        return link

    @staticmethod
    def get_price(item: Dict[str, Any], id: int) -> Union[float, None]:
        try:
            price = item[id]["price"][0]["price"]
        except:
            price = None
        return price

    @staticmethod
    def get_wine_style(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            item_style = item[id]["itemStyle"]
        except:
            item_style = None
        return item_style

    @staticmethod
    def get_wine_body(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            body = item[id]["itemBody"]
        except:
            body = None
        return body

    @staticmethod
    def get_wine_taste(item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            taste = item[id]["itemTasteProfile"]
        except:
            taste = None
        return taste

    @staticmethod
    def get_stock(item: Dict[str, Any], id: int) -> Union[int, None]:
        try:
            stock = item[id]["stockLevel"][0]["stock"]
        except:
            stock = None
        return stock

    @staticmethod
    def get_categories_dict(item: Dict[str, Any], id: int) -> dict:
        """
        Loops through the list of dictionaries of categories for each item.
        Grabs types and names of each feature and returns a dictionary.
        """
        types, names = ([] for _ in range(2))

        try:
            item_categories = item[id]["categories"]
            for feature in range(len(item_categories)):
                types.extend([item_categories[feature]["type"]])
                names.extend([item_categories[feature]["name"]])

                if item_categories[feature]["type"] == "REGION":
                    extracted_country = [
                        item_categories[feature]["storefrontUrl"].split("/")[2].title()
                    ]
                    types.extend(["COUNTRY"])
                    names.extend(extracted_country) if len(
                        extracted_country
                    ) != 0 and extracted_country != ["c"] else names.extend([None])

            categories_dict = {key: value for key, value in zip(types, names)}
        except:
            categories_dict = {}
        return categories_dict

    def get_region(self, item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            region = self.get_categories_dict(item, id)["REGION"]
        except:
            region = None
        return region

    def get_country(self, item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            country = self.get_categories_dict(item, id)["COUNTRY"]
        except:
            country = None
        return country

    def get_wine_type(self, item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            wine_type = self.get_categories_dict(item, id)["PRODUCT_TYPE"]
        except:
            wine_type = None
        return wine_type

    def get_varietal(self, item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            varietal = self.get_categories_dict(item, id)["VARIETAL_TYPE"]
        except:
            varietal = None
        return varietal

    def get_varietal_style(self, item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            varietal_style = self.get_categories_dict(item, id)["STYLE"]
        except:
            varietal_style = None
        return varietal_style

    def get_appelation(self, item: Dict[str, Any], id: int) -> Union[str, None]:
        try:
            appelation = self.get_categories_dict(item, id)["APPELLATION"]
        except:
            appelation = None
        return appelation

    def get_one_item_data(self, item: Dict[str, Any], id: int) -> dict:
        item_data_dict = {
            "title": self.get_title(item, id),
            "year": self.get_production_year(item, id),
            "price": self.get_price(item, id),
            "customer_rating": self.get_star_average(item, id),
            "reviews": self.get_review_count(item, id),
            "score": self.get_rating_score(item, id),
            "winery_direct": self.is_winery_direct(item, id),
            "stock": self.get_stock(item, id),
            "brand": self.get_brand(item, id),
            "country/state": self.get_country(item, id),
            "region": self.get_region(item, id),
            "appelation": self.get_appelation(item, id),
            "wine_type": self.get_wine_type(item, id),
            "varietal": self.get_varietal(item, id),
            "varietal_style": self.get_varietal_style(item, id),
            "style": self.get_wine_style(item, id),
            "taste": self.get_wine_taste(item, id),
            "body": self.get_wine_body(item, id),
            "description": self.get_description(item, id),
            "img": self.get_img_link(item, id),
            "link": self.get_item_link(item, id),
        }
        return item_data_dict

    def scrape_items(self) -> pd.DataFrame:
        """
        Scrapes products for each page and each given wine type and returns a dataframe.
        """
        data = []
        item_types = self.item_types

        for wine_type in item_types:

            for page in range(1, (self.number_of_pages + 1)):
                item = self.get_products(page, wine_type)

                for id in range(self.items_per_page):
                    data.append(self.get_one_item_data(item, id))

            time.sleep(np.random.uniform(2, 7))

        dataframe = pd.DataFrame(data=data)
        return dataframe.iloc[: self.items_to_return]

    @staticmethod
    def get_csv(df: pd.DataFrame, path: str) -> None:
        """
        Saves a created csv file in the given location.

        Args:
            df (pd.DataFrame): dataframe with the scraped data.
            path (str): location on the device to save created csv.
        """
        return df.to_csv(os.path.join(path, r"totalwine_data.csv"))
