import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.youtube["items"][0]["snippet"]["title"]
        self.description = self.youtube["items"][0]["snippet"]["description"]
        self.url = self.youtube["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        self.subscriber_count = self.youtube["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.youtube["items"][0]["statistics"]["videoCount"]
        self.view_count = self.youtube["items"][0]["statistics"]["viewCount"]
        self.data = {"title": self.title, "description": self.description, "url": self.url,
                     "subscriber_count": self.subscriber_count, "video_count": self.video_count,
                     "view_count": self.view_count}

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube))

    @classmethod
    def get_service(cls):
        """
         класс-метод ,
         возвращающий объект для работы с YouTube API
        """
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
           self.__channel_id = channel_id

    def to_json(self, filename) -> None:
        """
         метод, сохраняющий в файл значения
         атрибутов экземпляра `Channel`
        """
        with open(filename, "w") as file:
            json.dump(self.youtube, file, indent=2, ensure_ascii=False)

