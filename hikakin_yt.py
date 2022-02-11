from cgitb import reset
from dis import disco
from apiclient import discovery
import json

from numpy import block
import config
import html
import re

YOUTUBE_API_SERVICE_NAME='youtube'
YOUTUBE_API_VERSION='v3'

HIKAKIN_YT_ID='UCZf__ehlCEBPop-_sldpBUQ'
SEIKIN_YT_ID='UCg4nOl7_gtStrLwF0_xoV0A'

youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=config.YOUTUBE_API_KEY)

def format_text(t):
    t = t.replace('　', ' ')  # Full width spaces
    # t = re.sub(r'([。．！？…]+)', r'\1\n', t)  # \n after ！？
    t = re.sub(r'(.+。) (.+。)', r'\1 \2\n', t)
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'([。．！？…])\n」', r'\1」 \n', t)  # \n before 」
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'\n+', r'\n', t).rstrip('\n')  # Empty lines
    t = re.sub(r'\n +', '\n', t)  # Spaces
    return t

def get_channel_videos(channel_id: str, block_num: int):
    results = []
    nextPageToken = ''
    for i in range(block_num):
        kwargs = {
            'channelId': channel_id,
            'type': 'video',
            'part': 'id,snippet',
            'maxResults': 50
        }

        if nextPageToken:
            kwargs['pageToken'] = nextPageToken

        res = youtube.search().list(
            **kwargs
        ).execute()

        results.extend(res['items'])

        nextPageToken = res.get('nextPageToken')
    return results

def getTitlesArray(items: list):
    r = []
    for item in items:
        if item['id']['kind'] == 'youtube#video':
            r.append(format_text(html.unescape(item['snippet']['title']).replace('【', '').replace('】', '')))
    return r

videoTitles = []

videoTitles.extend(getTitlesArray(get_channel_videos(HIKAKIN_YT_ID, 20)))
videoTitles.extend(getTitlesArray(get_channel_videos(SEIKIN_YT_ID, 20)))
print(f'Fetched {len(videoTitles)} videos')

with open('input.txt', 'w', encoding='utf8') as f:
    f.write('\n'.join(videoTitles))

print('OK')