import pytest
from totalwine_scraper.scraper import Scraper
import pandas as pd


def test_number_of_items():
    scraper = Scraper(200, ["red"])
    assert scraper.number_of_items == 200


def test_item_types():
    scraper = Scraper(200, ["reD", "w hItE"])
    assert scraper.item_types == ["Red", "White"]


def test_number_of_pages():
    scraper = Scraper(250, ["red"])
    assert scraper.number_of_pages == 2


def test_items_to_return():
    scraper = Scraper(250, ["red", "white"])
    assert scraper.items_to_return == 500


def test_get_headers():
    scraper = Scraper(200, ["red"])
    headers = scraper.get_headers(2, "Red")
    true_headers = {
        "authority": "www.totalwine.com",
        "sec-ch-ua": "^\\^",
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"https://www.totalwine.com/wine/c/c0020?&page=1&pageSize=200&department=Wine&producttype=Red^%^20Wine&aty=1,1,0,1",
        "accept-language": "en-US,en;q=0.9",
    }
    assert headers == true_headers


def test_get_params():
    scraper = Scraper(200, ["Red", "White"])
    params = scraper.get_params(3, "White")
    true_params = (
        ("page", "3"),
        ("pageSize", "200"),
        ("state", "US-CA"),
        ("shoppingMethod", "INSTORE_PICKUP^%^2CDELIVERY"),
        ("userShoppingMethod", "INSTORE_PICKUP"),
        ("allStoresCount", "true"),
        ("searchAllStores", "true"),
        ("storeId", "1108"),
        ("department", "Wine"),
        ("producttype", "White^%^20Wine"),
    )
    assert params == true_params


def test_get_response():
    scraper = Scraper(199, ["Red"])
    response = scraper.get_response(2, "Red")
    assert response.status_code == 200