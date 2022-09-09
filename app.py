import time
from lalafo import Lalafo

from loader import db_handler


def main():
    lalafo_service = Lalafo()

    while True:
        categories = db_handler.get_categories()
        for cat in categories:
            lalafo_service.get_offers_from_filter_page(cat)

        time.sleep(3)


if __name__ == '__main__':
    main()