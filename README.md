# Totalwine.com scraper

![alt text](https://www.totalwine.com/media/sys_master/cmsmedia/h4d/h16/8994184232990.jpg)

## Purpose

This package is ready to scrape totalwine.com for demanded number of listings with the given wine types.


## Installation
```
git clone git@github.com:Karalius/totalwine-scraper.git
pip install -r requirements.txt
cd totalwine_scraper
pip install
```

## Usage
```
from totalwine_scraper import Scraper

scraper = Scraper(200, ['red', 'white'])
df = scraper.scrape_items()
```

## Output as JSON

This example shows one listing's scraped information in JSON format.

```
output = {
        "title": "14 Hands Chardonnay",
        "year": null,
        "price": 9.97,
        "c_rating": 4.6,
        "reviews": 20,
        "score": null,
        "winery_direct": 0,
        "stock": 49,
        "brand": "14 Hands",
        "country/state": null,
        "region": null,
        "appelation": null,
        "wine_type": "White Wine",
        "varietal": "Chardonnay",
        "varietal_style": null,
        "style": "Elegant",
        "taste": "Apple, Toast",
        "body": "Medium-bodied",
        "description": "Washington- Bright apple and floral aromas are complemented by light notes of vanilla and sweet butterscotch. Juicy pear and apple flavors give way to subtle touches of toast and spice and ends with a soft finish.",
        "img": "https://www.totalwine.com/media/sys_master/twmmedia/hc6/h9e/14536635908126.png",
        "link": "https://www.totalwine.com/wine/white-wine/chardonnay/14-hands-chardonnay/p/16940750"
    }
```

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

