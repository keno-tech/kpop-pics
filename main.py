from moviepy.editor import *
import glob
import subprocess
import os
import random
import praw
import urllib.request


# Scrape images of idols on reddit into kpics folder
def scrape_reddit(client_id, client_secret, folder):
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret, user_agent="my_user_agent")
    subreddit = reddit.subreddit("kpics")
    count = 0
    for submission in subreddit.new(limit = None):
        if count > 10:
            title = submission.title
            if len(title) > 100:
                title = f"My Idol{count}"
            url = str(submission.url)
            if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
                # Retrieve the image and save it in folder
                fullfilename = os.path.join('kpics', f'{title}.png')
                urllib.request.urlretrieve(url, fullfilename)
                count += 1

                # Stop once you have 10 images
                if count == 20:
                    break
        else:
            count += 1
    return



# Take photos of smiling for the initial video part
def initial_video(folder, duration):
    smiling = glob.glob(f'{folder}/*.jpg')
    initial_image = ImageClip(random.choice(smiling)).set_duration(duration).resize(width=1280, height=720)
    initial_clip = initial_image.crossfadein(0.2)
    txt_clip = TextClip("yo bro who got you smiling like that", fontsize= 22, color = 'black', bg_color='white', font='Calisto-MT').set_position(('center')).set_duration(duration)
    initial_clip = CompositeVideoClip([initial_clip, txt_clip])
    return initial_clip

def second_video(folder, duration):
    kpics = glob.glob(f'{folder}/*.png')
    clips = []
    for pic in kpics:
        image = ImageClip(pic).set_duration(duration).resize(width=1280, height=720)
        txt_clip = TextClip(f"{os.path.basename(pic)[:-4]}", fontsize= 52, color = 'white', bg_color='black', font='Calisto-MT').set_position(('center', 'bottom')).set_duration(duration)
        image = CompositeVideoClip([image, txt_clip])
        clips.append(image)

    second_video = concatenate_videoclips(clips, method='compose')
    return second_video

def connect_videos(videos):
    final_video = concatenate_videoclips(videos, method='compose')
    return final_video

def set_audio(final_video, music, duration):
    audio = AudioFileClip(music)
    audio = audio.subclip(0, duration)
    audio = audio.volumex(0.6)
    final_video = final_video.set_audio(audio)

    return final_video

scrape_reddit(client_id = "cbTHQbT76pk7dWtBdiOgdA", client_secret = "G2oemMyP25hPVtQFcTTc_AUKVeNxVA", folder='kpics')
videos = []
videos.append(initial_video(folder= 'smiling', duration = 4))
videos.append(second_video(folder= 'kpics', duration = 1))

final_video = connect_videos(videos)

final_video = set_audio(final_video, music= 'smiling_song.mp3', duration= 15)
final_video.write_videofile('final_output.mp4', fps=24)

subprocess.run(['ffmpeg', '-i', 'final_output.mp4', '-vf', 'crop=405:720', f'YT_SHORT.mp4'])
os.remove('final_output.mp4')