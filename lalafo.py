from loguru import logger
from loader import req, db_handler
from utils import stopwatch
from offer import Offer

import telegram


class Lalafo:
    def __init__(self):
        self.req = req

    @stopwatch
    def get_offers_from_filter_page(self, url):
        logger.debug(f'Collecting offers from the category - {url}')

        resp = self.req.get(url)
        resp_dict = dict(resp.json())

        viewed_ids = db_handler.get_viewed_links()

        for item in resp_dict['items']:
            offer = Offer('https://lalafo.kg' + item['url'])
            offer.id = str(item['id'])

            if offer.id in viewed_ids:
                logger.debug(f'{offer.id} - found in db, offer will be skipped')
                continue
            else:
                offer.title = item['title']
                offer.description = item['description']
                offer.price = item['price']
                offer.number = item.get('number', None)
                offer.seller_id = item['user_id']

                try:
                    offer.photo = item.get('images')[0]['original_url']
                except IndexError:
                    offer.photo = 'https://tdolis.ru/assets/img/nophoto.png'


                try:
                    telegram.send_offer(offer)

                except Exception:
                    pass
                else:
                    db_handler.add_to_viewed_links(offer.id)

        try:
            next_page = 'https://lalafo.kg' + resp_dict['_links']['next']['href']

        except KeyError:
            return None
        else:
            return next_page


def main():
    lalafo = Lalafo()
    url = 'https://lalafo.kg/api/search/v3/feed/search?category_id=4311&city_id=103184&currency=KGS&expand=url&page=1'

    result = lalafo.get_offers_from_filter_page(url)
    print(result)

if __name__ == '__main__':
    main()