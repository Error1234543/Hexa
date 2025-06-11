import os
import time
import psutil

def is_authorized(user_id, chat_id, owner_id, allowed_group, allowed_users):
    return user_id == owner_id or chat_id == allowed_group or user_id in allowed_users

def add_authorized_user(user_id, authorized_users):
    authorized_users.add(user_id)

def extract_filename(url):
    return url.split('/')[-1].split('?')[0].replace('.m3u8', '').replace('.pdf', '')

def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02}:{mins:02}:{secs:02}"
