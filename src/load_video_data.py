import os
import shutil
import random
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
from tqdm import tqdm
from urllib.parse import urljoin, urlsplit

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, 'data')
videos_per_playlist = 10
playlist_list = ['multivariable_calculus',
                 'physics',
                 'electrical_engineering',
                 'grammar',
                 'chemistry',
                 'finance',
                 'biology',
                 'microeconomics_and_macroeconomics',
                 'history',
                 'cryptography']


def underscore(string):
    return '_'.join(string.lower().split())

channel_url = 'https://www.youtube.com/user/khanacademy/playlists'
base_url = '{0.scheme}://{0.netloc}/'.format(urlsplit(channel_url))
channel_page = requests.get(channel_url)
channel_soup = BeautifulSoup(channel_page.content, 'html.parser')
playlist_links = channel_soup.find_all(class_='yt-uix-tile-link')
playlist_names = [underscore(link.getText()) for link in playlist_links]
playlist_pairs = zip(playlist_links, playlist_names)
chosen_pairs = filter(lambda pair: pair[1] in playlist_list, playlist_pairs)

for playlist_link, playlist_name in tqdm(chosen_pairs): 
    playlist_dir  = os.path.join(data_dir, playlist_name)
    playlist_url = urljoin(base_url, playlist_link['href'])
    playlist_page = requests.get(playlist_url)
    playlist_soup = BeautifulSoup(playlist_page.content, 'html.parser')
    video_links = playlist_soup.find_all(class_='yt-uix-tile-link')

    try:
        os.mkdir(playlist_dir)
    except OSError:
        shutil.rmtree(playlist_dir)
        os.mkdir(playlist_dir)

    for video_link in tqdm(random.sample(video_links, videos_per_playlist)):
        video_url = urljoin(base_url, video_link['href'])
        yt = YouTube(video_url)
        yt.set_filename(underscore(yt.filename.split('  ')[0]))
        video = yt.get('mp4', '360p')
        video.download(playlist_dir)
