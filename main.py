from re import sub
from typing import Text
from reddit.Reddit import Reddit
from video.TextToSpeech import TextToSpeech
from video.Video import Video
from youtube.Youtube import Youtube
import os

reddit = Reddit()

subreddit = 'AskReddit'
submission = reddit.get_comments(subreddit)

tts_texts = submission.get_tts_texts()
full_tts_text = submission.get_full_tts_text()
tts = TextToSpeech()
folder = os.path.join('files', submission.title)
os.makedirs(folder, exist_ok=True)
video = Video(save_path=folder)

audio_file = os.path.join(folder, f'audio.mp3')
tts.save(full_tts_text, audio_file)

duration = tts.get_duration(submission.title)
video.add_text(submission.title, submission.title, submission.author.icon_img, duration)


for index_1, comments in enumerate(tts_texts):
    comment_text = ''
    for index_2, text in enumerate(comments['text']):
        duration = tts.get_duration(text)
        comment_text += text + ' '
        video.add_text(comment_text, ' '.join(text), comments['profile_img_url'], duration)

video.add_audio_and_save(audio_file)

youtube = Youtube()

title = f'{submission.title} (r/{subreddit}) #shorts'
description = f'Reddit shorts from r/{subreddit}: {submission.title} #shorts'
keywords = ['#shorts', 'Reddit', subreddit]

youtube.upload_video(file = os.path.join(folder, 'video.mp4'), 
                     title = title, 
                     description = description,
                     keywords = keywords)

