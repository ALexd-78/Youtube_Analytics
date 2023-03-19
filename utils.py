import os
import json
import pprint
import isodate
import datetime

from googleapiclient.discovery import build



class Channel:

    # channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
    # channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'  # Редакция

    def __init__(self, channel_id):
        self.__channel_id = channel_id

        # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('API_KEY')
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        # инициализация атрибутов класса при создании экземпляра класса
        self.__channel_id = self.channel['items'][0]['id']  # id канала
        self.title = self.channel['items'][0]['snippet']['title']  # название канала
        self.description = self.channel['items'][0]['snippet']['description']  # описание канала
        self.channel_link = 'https://www.youtube.com/channel/' + self.channel['items'][0]['id']  # ссылка на канал
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount']  # количество видео
        self.view_count = self.channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def __str__(self) -> str:
        '''Выводит информацию для пользователя о канале'''
        return f'Youtube-канал: {self.title}'

    def __lt__(self, other) -> int:
        '''Сравнивает каналы по количеству подписчиков'''
        return self.subscriber_count > other.subscriber_count

    def __add__(self, other) -> int:
        '''Складывает каналы по количеству подписчиков'''
        return int(self.subscriber_count) + int(other.subscriber_count)

    def print_info(self):
        '''Выводит информацию о канале в JSON-формат'''
        return json.dumps(self.channel, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        '''Запрещает внесение изменений в id канала'''
        return self.__channel_id

    @classmethod
    def get_service(cls):
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
            'channel_link': self.channel_link,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


class VIDError(Exception):
    pass

class Video:
    def __init__(self, video_id: str):
        self.video_id = video_id
        try:
            youtube = Channel.get_service()
            self.video_response = youtube.videos().list(id=self.video_id, part='snippet,statistics',).execute()
            self.video_title: str = self.video_response['items'][0]['snippet']['title']
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except:
            self.video_title = None
            self.view_count = None
            self.like_count = None

    def __str__(self) -> str:
        '''Выводит информацию для пользователя о видео'''
        return self.video_title

class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        youtube = Channel.get_service()
        playlist_info = youtube.playlists().list(id=playlist_id, part='snippet, contentDetails, status').execute()
        self.playlist_title = playlist_info['items'][0]['snippet']['title']


    def __str__(self) -> str:
        '''Выводит информацию для пользователя о плейлисте'''
        return f'{self.video_title} ({self.playlist_title})'


class PlayList():
    '''Обработка данных плейлиста'''
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        youtube = Channel.get_service()
        self.playlist = youtube.playlists().list(id=self.playlist_id, part='snippet',).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist_video = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()
        # получает все id видеороликов из плейлиста
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_video['items']]
        # выводит длительность видеороликов из плейлиста
        self.video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()


    @property
    def total_duration(self):
        total_duration = datetime.timedelta()

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration


    def show_best_video(self):

        videos = {}
        for i in range(len(self.video_ids)):
            videos[int(self.video_response['items'][i]['statistics']['likeCount'])] = self.video_ids[i]

        return f"https://www.youtube.com/watch?v={videos[max(videos)]}"


broken_video = Video('broken_video_id')
print(broken_video.video_title)
print((broken_video.like_count))


# video1 = Video('9lO06Zxhu88')
# print(video1)