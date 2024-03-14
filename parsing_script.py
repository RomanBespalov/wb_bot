import logging

import aiohttp


async def get_product_info(article):
    base_url = "https://card.wb.ru/cards/v1/detail"
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 30,
        "nm": article,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                response.raise_for_status()
                logging.info(f"Запрос к сайту {base_url} с артикулом - {article}")

                if response.status == 200:
                    product_info = await response.json()
                    attribute = product_info.get('data').get('products')[0]
                    product_data = {
                        'название': attribute.get('name'),
                        'артикул': attribute.get('id'),
                        'цена': f"{attribute.get('salePriceU') // 100} руб",
                        'рейтинг товара': f"{attribute.get('reviewRating')}⭐",
                        'количество товара': f"{attribute.get('sizes')[0].get('stocks')[0].get('qty')} шт.",
                    }
                    logging.info("Получение данных из json")
                    return product_data

    except aiohttp.ClientError as e:
        logging.error(f"Возникла ошибка при запросе к сайту {base_url} - {e}")

    except (AttributeError, IndexError) as e:
        logging.error(f"Ошибка в обработке данных - {e}")
        return "Ошибка в обработке данных"


# Синхронный код
"""import logging
import sys

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
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        logging.info(f"Запрос к сайту {base_url} с артикулом - {article}")

        if response.status_code == 200:
            product_info = response.json()
            attribute = product_info.get('data').get('products')[0]
            product_data = {
                'название': attribute.get('name'),
                'артикул': attribute.get('id'),
                'цена': f"{attribute.get('salePriceU') // 100} руб",
                'рейтинг товара': f"{attribute.get('reviewRating')}⭐",
                'количество товара': f"{attribute.get('sizes')[0].get('stocks')[0].get('qty')} шт.",
            }
            logging.info("Получение данных из json")
            return product_data

    except requests.exceptions.RequestException as e:
        logging.error(f"Возникла ошибка при запросе к сайту {base_url} - {e}")

    except (AttributeError, IndexError) as e:
        logging.error(f"Ошибка в обработке данных - {e}")
        return "Ошибка артикула"
"""
