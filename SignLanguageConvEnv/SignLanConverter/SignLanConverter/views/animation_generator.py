from math import floor
import os
import time
from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.http import HttpResponse
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from .change_video_speed import speed_up_video

def convert_tokens_to_mp4(request, tokens, video_name,original_audio_duration):
    start_mp4_time = time.time()
    used_language = request.POST.get('language')
    used_language = used_language[:2]
    tokens_mp4 = {}
    folder_name = f"assets\{used_language}"
    for token in tokens:
        if token in tokens_mp4:
            continue
        filename = token + ".mp4"
        filepath = os.path.join(folder_name, filename)
        if os.path.exists(filepath):
            tokens_mp4[token] = filepath
        else:
            for letter in token:
                if letter != 'l':
                    word_letter = letter + '.mp4'
                    letter_path = os.path.join(folder_name, word_letter)
                    tokens_mp4[letter] = letter_path
    # Load each video clip using VideoFileClip
    video_clips = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for path in tokens_mp4.values():
            if os.path.exists(path):
                futures.append(executor.submit(VideoFileClip, path))
        for future in futures:
            video_clips.append(future.result())
    # Concatenate the clips into a single video using concatenate_videoclips
    final_clip = concatenate_videoclips(video_clips)

    final_clip_path = os.path.join(
        settings.MEDIA_ROOT, 'sign_language_videos', video_name + '.mp4')

    final_clip.write_videofile(final_clip_path)

    # Generate the URL of the final video file
    video_absolute_url = request.build_absolute_uri(
        settings.MEDIA_URL + 'sign_language_videos/')

    # print("duration ", int(final_clip.duration))
    
    original_audio_duration=floor(original_audio_duration)
    
    #you can change the output file speed by uncomment the next 5 lines of code, the next lines makes the 
    #output video the same duration as the original audio duration
    
    # print("original duration ", original_audio_duration)
    
    # speed_x = final_clip.duration / original_audio_duration

    # speed_x = round(1, 1)

    # print("speed_X ", speed_x)
    # speed_up_video(final_clip_path, speed_x)

    video_url = str(video_absolute_url) + video_name + '.mp4'

    # calculate time and memory used
    end_mp4_time = time.time()
    total_mp4_time = end_mp4_time - start_mp4_time

    print(f"Total convert tokens to mp4 time: {total_mp4_time:.2f} seconds")

    return video_url

