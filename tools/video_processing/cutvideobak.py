import os
import random
import psutil  # 用于检查文件锁定状态
from moviepy.editor import VideoFileClip, AudioFileClip

# 指定源视频和目标文件夹路径
source_folder = r'/volume2/Download/sucai/sleepykitty'
target_folder = r'/volume2/Download/sucai/douyin'
split_duration = 3599  # 每个短视频长度为3599秒
min_clip_duration = 3000  # 分割片段最小时长，50分钟（单位：秒）

# 读取 title.txt 的内容
script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本目录
title_file_path = os.path.join(script_dir, 'title.txt')  # 获取 title.txt 的路径
list_file_path = os.path.join(script_dir, 'list.txt')    # 获取 list.txt 的路径

with open(title_file_path, 'r', encoding='utf-8') as f:
    titles = f.read().split('##')  # 分割每个介绍

# 检查文件是否被锁定
def is_file_locked(file_path):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for file in proc.open_files():
                    if file.path == file_path:
                        print(f"文件 {file_path} 被进程 {proc.info['name']} (PID: {proc.info['pid']}) 占用，跳过处理。")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    except Exception as e:
        print(f"检查文件 {file_path} 锁状态时出错: {e}")
        return True  # 出现异常时，假设文件被锁定

# 获取已处理文件列表
def get_processed_files():
    if os.path.exists(list_file_path):
        with open(list_file_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    return set()

# 记录处理完成的文件
def record_processed_file(file_path):
    with open(list_file_path, 'a', encoding='utf-8') as f:
        f.write(file_path + '\n')

# 获取指定文件夹内的所有视频文件
def find_video_files(folder):
    video_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            # 排除以"."开头的临时文件夹和文件
            if file.startswith('.') or '.__jianying_export_temp_folder__' in root:
                print(f"跳过临时文件: {os.path.join(root, file)}")
                continue
            if file.endswith(('.mp4', '.avi', '.mov')):  # 根据需要添加更多视频格式
                video_files.append(os.path.join(root, file))
    return video_files

# 生成随机介绍内容的TXT文件
def create_txt_file(video_clip_name, target_path):
    random_title = random.choice(titles).strip()
    tags = "#入眠曲 #安静的音乐 #每日吸猫 #萌宠 #失眠"
    txt_content = f"{random_title}\n{tags}"

    txt_file_path = os.path.join(target_path, f'{video_clip_name}.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(txt_content)

# 处理单个视频文件
def process_video(video_path):
    relative_path = os.path.relpath(video_path, source_folder)
    target_path = os.path.join(target_folder, os.path.dirname(relative_path))
    os.makedirs(target_path, exist_ok=True)

    video = VideoFileClip(video_path)
    video_duration = video.duration

    # 获取视频帧率
    fps = video.fps or 30  # 如果 fps 是 None，使用默认帧率 30
    print(f"处理视频: {video_path}, 视频时长: {video_duration} 秒, 帧率: {fps}")
    
    video_name, video_ext = os.path.splitext(os.path.basename(video_path))

    start_time = 0
    clip_count = 1
    used_music = set()

    while start_time < video_duration:
        end_time = min(start_time + split_duration, video_duration)
        clip_duration = end_time - start_time

        if clip_duration < min_clip_duration:
            print(f"跳过时长小于 50 分钟的片段 {video_name}_{clip_count} ({clip_duration} 秒)")
            start_time += split_duration
            clip_count += 1
            continue

        output_file = os.path.join(target_path, f'{video_name}_{clip_count}{video_ext}')

        if os.path.exists(output_file):
            print(f"视频片段 {output_file} 已存在，跳过...")
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

        if music_clip.duration < video_clip.duration:
            music_clip = music_clip.audio_loop(duration=video_clip.duration)

        music_subclip = music_clip.subclip(0, video_clip.duration)
        video_with_new_audio = video_clip.set_audio(music_subclip)

        # 写入视频文件时指定帧率，并强制设置时长
        video_with_new_audio.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=fps, preset="slow", threads=4)

        create_txt_file(f'{video_name}_{clip_count}', target_path)

        record_processed_file(output_file)

        start_time += split_duration  # 保持严格的时间间隔
        clip_count += 1

    video.close()

# 获取音乐文件
music_files = [os.path.join(r'/volume1/homes/VideoMaterial/audiomaterial', f) for f in os.listdir(r'/volume1/homes/VideoMaterial/audiomaterial')
               if f.endswith(('.mp3', '.wav'))]

# 获取已处理文件列表
processed_files = get_processed_files()

# 遍历源目录并处理视频
video_files = find_video_files(source_folder)
for video_path in video_files:
    relative_path = os.path.join(target_folder, os.path.relpath(video_path, source_folder))
    if relative_path in processed_files:
        print(f"视频 {relative_path} 已处理过，跳过...")
        continue
    if is_file_locked(video_path):
        continue  # 如果文件被锁定，跳过处理
    process_video(video_path)

print("所有视频处理完成。")
