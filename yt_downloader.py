import os

from pytube import YouTube, Stream
import shutil
from moviepy.editor import AudioFileClip, VideoFileClip


class Downloader:

    def __init__(self, url):
        self.yt = YouTube(url,
                          on_progress_callback=Downloader.__on_update,
                          on_complete_callback=Downloader.__on_complete)

    @staticmethod
    def __on_update(stream, chunk, remains):
        total = stream.filesize
        progress = ((total - remains) / total) * 100
        log = 'downloading {file_type}... {percent:05.2f}%'.format(file_type=stream.type, percent=progress)
        print('\r', end='')
        print(log, end='')

    @staticmethod
    def __on_complete(stream: Stream, file_path):
        print('\nsuccessfully downloaded {file_type} from {title}'.format(file_type=stream.type, title=stream.title))

    def download_video(self, resolution='highest', video_type='mp4', output_dir='./', video_name=None):
        if resolution == 'highest':
            stream = self.yt.streams.filter(subtype='mp4', adaptive=True, type='video').first()
        else:
            stream = self.yt.streams.filter(subtype='mp4', resolution=resolution, type='video').first()

        if video_name is None:
            video_name = stream.default_filename
        else:
            video_name = '{name}.{type}'.format(name=video_name, type=video_type)

        video_path = os.path.join(output_dir, video_name)
        if os.path.exists(video_path):
            return video_path, VideoFileClip(video_path).duration

        # here we create the cache path and so the output path would be created at the same time
        cache_path = os.path.join(output_dir, 'cache/')
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        temp_video = stream.download(output_path=cache_path, filename='temp_video.mp4')
        video = VideoFileClip(temp_video)
        duration = video.duration

        if stream.is_adaptive:
            temp_audio = self.yt.streams.filter(subtype='mp4', type='audio').first().download(output_path=cache_path)

            print('Now writing the audio into video... ')
            audio = AudioFileClip(temp_audio)
            result_video = video.set_audio(audio)
            result_video.write_videofile(video_path)

            result_video.close()
            audio.close()
        else:
            os.rename(src=temp_video, dst=video_path)

        video.close()

        shutil.rmtree(cache_path)
        return video_path

    def download_audio(self, audio_type='mp3', output_dir='./', audio_name=None):
        stream = self.yt.streams.filter(subtype='mp4', type='audio').first()

        cache_path = os.path.join(output_dir, 'cache/')
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        temp_video_path = stream.download(output_path=cache_path)

        if audio_name is None:
            audio_name = stream.default_filename.replace('mp4', audio_type)
        else:
            audio_name = '{name}.{type}'.format(name=audio_name, type=audio_type)

        audio = AudioFileClip(temp_video_path)
        duration = audio.duration

        audio_path = os.path.join(output_dir, audio_name)

        # do not use ffmpeg codec 'libfdk_aac'
        if audio_type == 'm4a':
            audio.close()
            os.rename(temp_video_path, audio_path)
            return audio_path, duration

        audio.write_audiofile(audio_path)
        audio.close()
        # clean cache
        shutil.rmtree(cache_path, ignore_errors=True)

        return audio_path, duration
