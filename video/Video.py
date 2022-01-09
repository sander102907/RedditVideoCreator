import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
from video.VideoText import VideoText
from video.VideoImage import VideoImage
import moviepy.editor as mp
import os


class Video:
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 24, save_path: str = '/') -> None:
        self.width = width
        self.height = height
        self.fps = fps
        self.save_path = save_path

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fourcc = VideoWriter_fourcc(*'mp4v')
        self.video = VideoWriter(os.path.join(save_path, 'video_no_audio.mp4'), self.fourcc, float(fps), (width, height))


    def add_text(self, text: str, complete_text: str, profile_img_url: str, seconds: float) -> None:
        frame = np.full(shape=(self.height, self.width, 3), fill_value=20, dtype=np.uint8)
        frame = VideoText.draw_text(frame, text, complete_text, fontScale=1.2, thickness=2)
        profile_img = VideoImage.url_to_image(profile_img_url)
        frame[0:profile_img.shape[0], 0:profile_img.shape[0]] = profile_img

        for _ in range(int(self.fps * seconds)):
            self.video.write(frame)




    def add_audio_and_save(self, audio_file: str) -> None:
        self.video.release()

        audio = mp.AudioFileClip(audio_file)
        video = mp.VideoFileClip(os.path.join(self.save_path, 'video_no_audio.mp4'))
        video = video.set_audio(audio)
        video.write_videofile(os.path.join(self.save_path, 'video.mp4'))