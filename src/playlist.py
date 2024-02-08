import os
import json
from dotenv import load_dotenv
import isodate
import datetime
from googleapiclient.discovery import build


class PlayList:
    """Класс для ютуб-канала"""
    load_dotenv()
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        self.playlist_info = self.youtube.playlists().list(id=playlist_id, part='contentDetails, snippet', ).execute()
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails, snippet',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self._playlist_id}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        max_like_count = 0
        max_video_id = ''
        for video in self.video_response['items']:
            like_count: int = video['statistics']['likeCount']
            video_id = video['id']
            if int(like_count) > int(max_like_count):
                max_like_count = like_count
                max_video_id = video_id
        return f"https://youtu.be/{max_video_id}"
