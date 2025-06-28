import os
import random
import psutil  # Used to check file lock status
from moviepy.editor import VideoFileClip, AudioFileClip

# Specify source video and target folder paths
source_folder = r'/volume2/Download/sucai/sleepykitty'
target_folder = r'/volume2/Download/sucai/douyin'
split_duration = 3599  # Each short video length is 3599 seconds
min_clip_duration = 3000  # Minimum clip duration, 50 minutes (unit: seconds)

# Read the content of title.txt
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
title_file_path = os.path.join(script_dir, 'title.txt')  # Get the path of title.txt
list_file_path = os.path.join(script_dir, 'list.txt')    # Get the path of list.txt

with open(title_file_path, 'r', encoding='utf-8') as f:
    titles = f.read().split('##')  # Split each description

# Check if file is locked
def is_file_locked(file_path):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for file in proc.open_files():
                    if file.path == file_path:
                        print(f"File {file_path} is occupied by process {proc.info['name']} (PID: {proc.info['pid']}), skipping.")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    except Exception as e:
        print(f"Error checking lock status for file {file_path}: {e}")
        return True  # Assume file is locked if exception occurs

# Get processed file list
def get_processed_files():
    if os.path.exists(list_file_path):
        with open(list_file_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    return set()

# Record processed file
def record_processed_file(file_path):
    with open(list_file_path, 'a', encoding='utf-8') as f:
        f.write(file_path + '\n')

# Get all video files in the specified folder
def find_video_files(folder):
    video_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            # Exclude temp folders and files starting with "."
            if file.startswith('.') or '.__jianying_export_temp_folder__' in root:
                print(f"Skipping temp file: {os.path.join(root, file)}")
                continue
            if file.endswith(('.mp4', '.avi', '.mov')):  # Add more video formats as needed
                video_files.append(os.path.join(root, file))
    return video_files

# Generate random description TXT file
def create_txt_file(video_clip_name, target_path):
    random_title = random.choice(titles).strip()
    tags = "#SleepMusic #QuietMusic #DailyCat #CutePet #Insomnia"
    txt_content = f"{random_title}\n{tags}"

    txt_file_path = os.path.join(target_path, f'{video_clip_name}.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(txt_content)

# Process a single video file
def process_video(video_path):
    relative_path = os.path.relpath(video_path, source_folder)
    target_path = os.path.join(target_folder, os.path.dirname(relative_path))
    os.makedirs(target_path, exist_ok=True)

    video = VideoFileClip(video_path)
    video_duration = video.duration

    # Get video frame rate
    fps = video.fps or 30
    print(f"Processing video: {video_path}, duration: {video_duration} seconds, fps: {fps}")
    if fps is None or not isinstance(fps, (int, float)):
        print(f"Warning: Invalid fps for video {video_path}, using default 30.")
        fps = 30  # Set a default frame rate

    video_name, video_ext = os.path.splitext(os.path.basename(video_path))

    start_time = 0
    clip_count = 1
    used_music = set()

    while start_time < video_duration:
        end_time = min(start_time + split_duration, video_duration)
        clip_duration = end_time - start_time
        if clip_duration < min_clip_duration:
            print(f"Skipping clip {video_name}_{clip_count} ({clip_duration} seconds) less than 50 minutes")
            start_time += split_duration
            clip_count += 1
            continue

        output_file = os.path.join(target_path, f'{video_name}_{clip_count}{video_ext}')

        if os.path.exists(output_file):
            print(f"Video clip {output_file} already exists, skipping...")
            start_time += split_duration
            clip_count += 1
            continue

        video_clip = video.subclip(start_time, end_time)
        available_music = list(set(music_files) - used_music)
        if not available_music:
            used_music = set()
            available_music = music_files

        random_music = random.choice(available_music)
        used_music.add(random_music)
        music_clip = AudioFileClip(random_music)

        # Ensure music clip does not exceed split_duration
        if music_clip.duration < video_clip.duration:
            music_clip = music_clip.audio_loop(duration=video_clip.duration)
        else:
            music_clip = music_clip.subclip(0, min(video_clip.duration, split_duration))
        print(f"Music length: {music_clip.duration} ")
        print(f"Video length: {video_clip.duration} ")

        music_subclip = music_clip.subclip(0, video_clip.duration)
        video_with_new_audio = video_clip.set_audio(music_subclip)

        # Specify frame rate when writing video file
        video_with_new_audio.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=fps)

        create_txt_file(f'{video_name}_{clip_count}', target_path)

        record_processed_file(output_file)

        start_time += split_duration
        clip_count += 1

    video.close()


# Get music files
music_files = [os.path.join(r'/volume1/homes/VideoMaterial/audiomaterial', f) for f in os.listdir(r'/volume1/homes/VideoMaterial/audiomaterial')
               if f.endswith(('.mp3', '.wav'))]

# Get processed file list
processed_files = get_processed_files()

# Traverse source directory and process videos
video_files = find_video_files(source_folder)
for video_path in video_files:
    relative_path = os.path.join(target_folder, os.path.relpath(video_path, source_folder))
    if relative_path in processed_files:
        print(f"Video {relative_path} already processed, skipping...")
        continue
    if is_file_locked(video_path):
        continue  # Skip if file is locked
    process_video(video_path)

print("All videos processed.") 