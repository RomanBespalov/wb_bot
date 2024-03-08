import requests


def get_product_info(article):
    base_url = "https://card.wb.ru/cards/v1/detail"
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 30,
        "nm": article,
    }
    response = requests.get(base_url, params=params)
    product_info = response.json()
    try:
        product_data = {
            'название': product_info['data']['products'][0]['name'],
            'артикул': product_info['data']['products'][0]['id'],
            'цена': f"{product_info['data']['products'][0]['salePriceU'] // 100} руб",
            'рейтинг товара': f"{product_info['data']['products'][0]['reviewRating']}⭐",
            'количество товара': f"{product_info['data']['products'][0]['sizes'][0]['stocks'][0]['qty']} шт.",
        }
        return product_data
    except IndexError:
        return "Ошибка артикула"
