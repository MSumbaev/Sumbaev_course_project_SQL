import json

from utils import get_hh_data, create_database, save_data_to_database
from config import config


def main():

    employers_id = [
        '1740', # Яндекс
        # '80', # Альфа-Банк
        # '15478', # vk
        # '67611', # Тензор
        # '78638',# Tinkoff
        # '1057', # kaspersky
        # '3529', # Сбер
        # '3776', # MTC
        # '2180', # OZON
        # '4934' # билайн
    ]
    # params = config()

    print('Идет сбор данных...')
    data = get_hh_data(employers_id)
    # create_database('hh_ru', params)
    # save_data_to_database(data, 'hh_ru', params)

    def printj(obj) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(obj, indent=2, ensure_ascii=False))

    printj(data)


if __name__ == '__main__':
    main()
