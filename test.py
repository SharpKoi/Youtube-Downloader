from pytube import YouTube
from yt_downloader import Downloader

TEST_URL = 'https://www.youtube.com/watch?v=PdK2dqifYEs'
VIDEO_DIR = 'statics/video/'
AUDIO_DIR = 'statics/audio/'

downloader = Downloader(TEST_URL)
downloader.download_audio(output_dir=AUDIO_DIR, audio_name='星羅 Beautiful Wish')
