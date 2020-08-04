from pytube import YouTube
from yt_downloader import Downloader

VIDEO_DIR = 'media/video/'
AUDIO_DIR = 'media/audio/'

print('請輸入您要下載的網址: ', end='')
url = input()
print('請輸入您要下載的媒體類型: ', end='')
media_type = input()

downloader = Downloader(url)
if media_type == 'audio':
    audio_path, audio_len = downloader.download_audio(audio_type='m4a', output_dir=AUDIO_DIR)
    print(f'Path: {audio_path}')
    print(f'Duration: {audio_len}')
else:
    video_path, video_len = downloader.download_video(resolution='highest', output_dir=VIDEO_DIR)
    print(f'Path: {video_path}')
    print(f'Duration: {video_len}')
