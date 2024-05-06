import os
import json
import random
from bilibili import bilibili
from kuaishou import kuaishou
from douyin import douyin
from xiaohongshu import xiaohongshu


# Global variable to store uploaded video filenames
uploaded_videos = set()

def load_uploaded_videos():
    if os.path.exists('uploaded_videos.json'):
        with open('uploaded_videos.json', 'r') as file:
            return set(json.load(file))
    return set()

def save_uploaded_videos():
    with open('uploaded_videos.json', 'w') as file:
        json.dump(list(uploaded_videos), file)

def select_video_to_upload():
    videos_folder = r'C:\Users\lnx\Documents\code\myproject\englishwithantonio'

    videos = [f for f in os.listdir(videos_folder) if f.endswith('.mp4')]
    not_uploaded_videos = set(videos) - uploaded_videos
    if not_uploaded_videos:
        return os.path.join(videos_folder, random.choice(list(not_uploaded_videos)))
    return None

def upload_videos():
    video_to_upload = select_video_to_upload()
    if video_to_upload:
        douyin.dy_upload(video_to_upload)
        kuaishou.ks_upload(video_to_upload)
        xiaohongshu.xhs_upload(video_to_upload)
        bilibili.bl_upload(video_to_upload)
        uploaded_videos.add(os.path.basename(video_to_upload))
        save_uploaded_videos()
        os.remove(video_to_upload)  # Delete the uploaded video file
    else:
        print("No new videos to upload.")

if __name__ == "__main__":
    uploaded_videos = load_uploaded_videos()
    upload_videos()
