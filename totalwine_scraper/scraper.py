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
    def get_brand(item: Dict[str, Any], id: int, brands: list) -> list:
        try:
            brands.extend([item[id]["brand"]["name"]])
        except:
            brands.extend([None])
        return brands

    @staticmethod
    def get_star_average(item: Dict[str, Any], id: int, stars_average: list) -> list:
        try:
            stars_average.extend([item[id]["customerAverageRating"]])
        except:
            stars_average.extend([None])
        return stars_average

    @staticmethod
    def get_review_count(item: Dict[str, Any], id: int, reviews_count: list) -> list:
        try:
            reviews_count.extend([item[id]["customerReviewsCount"]])
        except:
            reviews_count.extend([None])
        return reviews_count

    @staticmethod
    def get_title(item: Dict[str, Any], id: int, titles: list) -> list:
        try:
            titles.extend([item[id]["name"]])
        except:
            titles.extend([None])
        return titles

    @staticmethod
    def get_production_year(item: Dict[str, Any], id: int, years: list) -> list:
        try:
            extract_year = item[id]["name"].split(", ")[1]
            years.extend([int(extract_year)])
        except:
            years.extend([None])
        return years

    @staticmethod
    def get_rating_score(item: Dict[str, Any], id: int, rating_scores: list) -> list:
        try:
            rating = item[id]["rating"]
            if rating != 0:
                rating_scores.extend([rating])
            else:
                rating_scores.extend([None])
        except:
            rating_scores.extend([None])
        return rating_scores

    @staticmethod
    def get_description(item: Dict[str, Any], id: int, descriptions: list) -> list:
        try:
            comment = [item[id]["review"]]
            if len(comment) != 0:
                descriptions.extend(comment)
            else:
                descriptions.extend([None])
        except:
            descriptions.extend([None])
        return descriptions

    @staticmethod
    def is_winery_direct(item: Dict[str, Any], id: int, winery_directs: list) -> list:
        try:
            winery_direct = item[id]["directType"]
            if winery_direct == "Winery Direct":
                winery_directs.extend([1])
            else:
                winery_directs.extend([0])
        except:
            winery_directs.extend([0])
        return winery_directs

    @staticmethod
    def get_img_link(item: Dict[str, Any], id: int, img_links: list) -> list:
        try:
            img_links.extend([item[id]["images"][0]["url"]])
        except:
            img_links.extend([None])
        return img_links

    @staticmethod
    def get_item_link(item: Dict[str, Any], id: int, links: list) -> list:
        try:
            full_link = "https://www.totalwine.com" + item[id]["productUrl"]
            links.extend([full_link])
        except:
            links.extend([None])
        return links

    @staticmethod
    def get_price(item: Dict[str, Any], id: int, prices: list) -> list:
        try:
            prices.extend([item[id]["price"][0]["price"]])
        except:
            prices.extend([None])
        return prices

    @staticmethod
    def get_wine_style(item: Dict[str, Any], id: int, item_styles: list) -> list:
        try:
            item_styles.extend([item[id]["itemStyle"]])
        except:
            item_styles.extend([None])
        return item_styles

    @staticmethod
    def get_wine_body(item: Dict[str, Any], id: int, bodies: list) -> list:
        try:
            bodies.extend([item[id]["itemBody"]])
        except:
            bodies.extend([None])
        return bodies

    @staticmethod
    def get_wine_taste(item: Dict[str, Any], id: int, tastes: list) -> list:
        try:
            tastes.extend([item[id]["itemTasteProfile"]])
        except:
            tastes.extend([None])
        return tastes

    @staticmethod
    def get_wine_stock(item: Dict[str, Any], id: int, stocks_available: list) -> list:
        try:
            stocks_available.extend([item[id]["stockLevel"][0]["stock"]])
        except:
            stocks_available.extend([None])
        return stocks_available

    @staticmethod
    def get_categories(
        item: Dict[str, Any],
        id: int,
        regions: list,
        wine_types: list,
        varietals: list,
        appelations: list,
        styles: list,
        countries: list,
    ) -> list:
        """
        Grabs all categories of each item and matches it with a given required categories: region, product_type, varietal_type, appelation, style.
        Returns extended lists for all categories with either grabbed value or None entry.
        """
        try:
            item_categories = item[id]["categories"]

            categories = [
                "REGION",
                "PRODUCT_TYPE",
                "VARIETAL_TYPE",
                "APPELLATION",
                "STYLE",
            ]
            lists_of_features = [regions, wine_types, varietals, appelations, styles]

            item_types, item_type_names, item_country = ([] for i in range(3))

            for item in range(len(item_categories)):

                item_types.extend([item_categories[item]["type"]])
                item_type_names.extend([item_categories[item]["name"]])

                if item_categories[item]["type"] == "REGION":
                    extracted_country = item_categories[item]["storefrontUrl"].split(
                        "/"
                    )[2]
                    item_country.extend([extracted_country])

            countries.extend(item_country) if len(
                item_country
            ) != 0 and item_country != ["c"] else countries.extend([None])

            wine_features_dict = {k: v for k, v in zip(item_types, item_type_names)}

            for i in range(len(categories)):
                feature = wine_features_dict.get(categories[i])
                if feature is not None:
                    lists_of_features[i].extend([feature])
                else:
                    lists_of_features[i].extend([None])
        except:
            regions.extend([None])
            wine_types.extend([None])
            varietals.extend([None])
            appelations.extend([None])
            styles.extend([None])
            countries.extend([None])

        return regions, wine_types, varietals, appelations, styles, countries

    def scrape_items(self) -> pd.DataFrame:
        """

        Main method of the class. Scrapes items and collects them in form of arrays, then transforms it to pandas DataFrame.

        Returns:
            pd.DataFrame: tabular data with all scraped listings and its features.
        """

        (
            titles,
            rating_scores,
            prices,
            years,
            img_links,
            links,
            winery_directs,
            descriptions,
            brands,
            countries,
            regions,
            appelations,
            wine_types,
            varietals,
            styles,
            tastes,
            bodies,
            item_styles,
            stars_average,
            reviews_count,
            stocks_available,
        ) = ([] for _ in range(21))

        item_types = self.item_types

        for wine_type in item_types:
            
            for page in range(1, (self.number_of_pages + 1)):
                item = self.get_products(page, wine_type)
                
                for id in range(self.items_per_page):
                    self.get_title(item, id, titles)
                    self.get_production_year(item, id, years)
                    self.get_price(item, id, prices)
                    self.get_star_average(item, id, stars_average)
                    self.get_review_count(item, id, reviews_count)
                    self.get_rating_score(item, id, rating_scores)
                    self.is_winery_direct(item, id, winery_directs)
                    self.get_wine_stock(item, id, stocks_available)
                    self.get_brand(item, id, brands)
                    self.get_wine_style(item, id, item_styles)
                    self.get_wine_taste(item, id, tastes)
                    self.get_wine_body(item, id, bodies)
                    self.get_description(item, id, descriptions)
                    self.get_img_link(item, id, img_links)
                    self.get_item_link(item, id, links)
                    self.get_categories(
                        item,
                        id,
                        regions,
                        wine_types,
                        varietals,
                        appelations,
                        styles,
                        countries,
                    )

                time.sleep(np.random.uniform(2, 7))

        dataframe = pd.DataFrame(
            {
                "title": titles,
                "year": years,
                "price": prices,
                "c_rating": stars_average,
                "reviews": reviews_count,
                "score": rating_scores,
                "winery_direct": winery_directs,
                "stock": stocks_available,
                "brand": brands,
                "country/state": countries,
                "region": regions,
                "appelation": appelations,
                "wine_type": wine_types,
                "varietal": varietals,
                "varietal_style": styles,
                "style": item_styles,
                "taste": tastes,
                "body": bodies,
                "description": descriptions,
                "img": img_links,
                "link": links,
            }
        )

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
