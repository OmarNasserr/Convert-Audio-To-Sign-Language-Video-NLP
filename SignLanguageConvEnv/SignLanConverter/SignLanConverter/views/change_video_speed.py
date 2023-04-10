from moviepy.editor import VideoFileClip

def speed_up_video(video_path, speed_factor):
    # Load the video clip
    clip = VideoFileClip(video_path)

    # Calculate the new duration of the clip based on the speed factor
    new_duration = clip.duration / speed_factor

    # Use the speedx method to speed up the clip by the specified factor
    new_clip = clip.speedx(speed_factor)

    # Set the duration of the new clip to the calculated value
    new_clip = new_clip.set_duration(new_duration)

    # Write the new clip to the specified output path
    new_clip.write_videofile("media\sign_language_videos\output.mp4")

    return new_clip