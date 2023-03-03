import os
import json
import pprint
import pprint

from googleapiclient.discovery import build


class Channel:

    # channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
    # channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'  # Редакция


    def __init__(self, channel_id):
        self.__channel_id = channel_id


        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key) # создать специальный объект для работы с API
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()


        #инициализация атрибутов класса при создании экземпляра класса
        self.__channel_id = self.channel['items'][0]['id']  #id канала
        self.title = self.channel['items'][0]['snippet']['title']  #название канала
        self.description = self.channel['items'][0]['snippet']['description']  #описание канала
        self.channel_link = 'https://www.youtube.com/channel/' + self.channel['items'][0]['id'] #ссылка на канал
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']  #количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount']  #количество видео
        self.view_count = self.channel['items'][0]['statistics']['viewCount']  #общее количество просмотров


    def __str__(self) -> str:
        '''Выводит информацию для пользователья о канале'''
        return f'Youtube-канал: {self.title}'


    def __gt__(self, other) -> int:
        '''Сравнивает каналы по количеству подписчиков'''
        print(self.subscriber_count < other.subscriber_count)


    def __add__(self, other) -> int:
        '''Складывает каналы по количеству подписчиков'''
        print(int(self.subscriber_count) + int(other.subscriber_count))

    def print_info(self):
        '''Выводим информацию о канале в JSON-формат'''
        return json.dumps(self.channel, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        '''Запрещает внесение изменений в id канала'''
        return self.__channel_id


    def get_service():
        '''получает объект для работы с API вне класса'''

        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def to_json(self, filename):
        '''Cоздаёт файл json с данными по каналу'''
        data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'channel_link':self.channel_link,
            'subscriber_count': self.subscriber_count,
            'video_count':self.video_count,
            'view_count':self.view_count
        }
        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

ch1 = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
ch2 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
# print(ch2)
ch1 > ch2
ch1 < ch2
ch1 + ch2

# vdud.print_info()

# print(vdud.title)
# print(vdud.description)
# print(vdud.channel_link)
# print(vdud.subscriber_count)
# print(vdud.video_count)
# print(vdud.view_count)

# vdud.channel_id = 'Новое название'


# print(Channel.get_service())

# vdud.to_json('vdud.json')