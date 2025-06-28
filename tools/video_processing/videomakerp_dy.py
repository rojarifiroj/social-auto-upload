import os
import random
import subprocess
from datetime import datetime
import sys
import logging

sys.stdout.reconfigure(encoding='utf-8')

# 日志配置
log_file = 'video_processing.log'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 路径配置
video_folder = r"/volume1/homes/VideoMaterial/cuuuestcat/SleepyCats/Cat's favorite music - Best music for cat 😽😽😽"
audio_folder = r'/volume1/homes/VideoMaterial/audiomaterial'
bgm_path = r'/volume1/homes/VideoMaterial/purring-cat-77928.mp3'
font_path = '/Windows/Fonts/youran.ttf'
watermark_text = "SleepyKitty"
output_folder = r'/volume2/Download/sucai/douyin'
record_file = 'processed_files.txt'  # 记录处理过的视频文件
progress_file = 'progress.txt'  # 记录每个视频的已处理进度

# 创建或读取记录文件，确保UTF-8编码
if not os.path.exists(record_file):
    open(record_file, 'w', encoding='utf-8').close()

if not os.path.exists(progress_file):
    open(progress_file, 'w', encoding='utf-8').close()

# 读取已处理文件列表
with open(record_file, 'r', encoding='utf-8') as f:
    processed_files = set(line.strip() for line in f)

# 读取处理进度
def read_progress():
    progress = {}
    with open(progress_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # 以最后一个逗号为分隔符，防止路径中包含逗号
                video_path, time_str = line.rsplit(',', 1)
                progress[video_path] = float(time_str)
            except ValueError:
                # 如果行的格式不正确，记录并跳过
                logging.warning(f"Skipping invalid progress line: {line.strip()}")
                continue
    return progress


# 更新处理进度
def update_progress(video_path, current_time):
    with open(progress_file, 'a', encoding='utf-8') as f:
        f.write(f"{video_path},{current_time}\n")

# 获取MP4文件列表
def get_mp4_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.mp4')]

# 获取随机音乐文件
def get_random_audio_file(folder):
    all_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.mp3'):
                all_files.append(os.path.join(root, file))
    return random.choice(all_files)

# 创建输出文件夹和文件名
def create_output_folder():
    now = datetime.now().strftime("%m%d%H%M")
    output_subfolder = os.path.join(output_folder, f"{now}p")
    os.makedirs(output_subfolder, exist_ok=True)
    logging.info(f"Created output folder: {output_subfolder}")
    return output_subfolder, now

# 处理视频并分割
def process_video(input_file, start_time=0):
    try:
        video_duration = get_video_duration(input_file)
        output_subfolder, now = create_output_folder()

        clip_count = 1

        while start_time + 3599 <= video_duration:
            final_output = os.path.join(output_subfolder, f"{now}p_{clip_count}.mp4")
            new_metadata_title = f"{now}p_{clip_count}"

            audio1 = bgm_path
            audio2 = get_random_audio_file(audio_folder)
            print(f"str(start_time): {str(start_time)}")
           

            # 合成视频和音频，截取 3599 秒
            cmd = [
                'ffmpeg', '-y', '-i', input_file, '-i', audio1, '-i', audio2,
                '-vf', f"fade=t=in:st=0:d=5, drawtext=text='{watermark_text}':fontfile={font_path}:x=10:y=10:fontsize=48:fontcolor=white@0.5",
                '-filter_complex', 
                f"[1:a]aloop=loop=-1:size=2e+09[a1]; [2:a]aloop=loop=-1:size=2e+09[a2]; [a1]volume=0.8[a1v]; [a1v][a2]amerge=inputs=2[a]",
                '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-b:v', '3000k', '-c:a', 'aac', '-shortest', '-r', '30',
                '-ss', str(start_time), '-to', str(start_time + 3599), '-metadata', f'title={new_metadata_title}', final_output
            ]
            subprocess.run(cmd)

            logging.info(f"Processed clip: {final_output}")

            start_time += 3599
            clip_count += 1
            update_progress(input_file, start_time)

        # 如果剩余不足 3599 秒，跳过该片段
        if video_duration - start_time < 3599:
            logging.info(f"Skipping remainder of {input_file} due to short length ({video_duration - start_time}s)")

        # 记录已处理文件
        with open(record_file, 'a', encoding='utf-8') as f:
            f.write(input_file + '\n')

        logging.info(f"Completed processing video: {input_file}")

    except Exception as e:
        logging.error(f"Error processing video: {input_file}, Error: {e}")

# 获取视频时长
def get_video_duration(video_file):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
           '-of', 'default=noprint_wrappers=1:nokey=1', video_file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

# 处理所有视频文件
def process_files():
    mp4_files = sorted(get_mp4_files(video_folder))
    progress = read_progress()

    for video_file in mp4_files:
        if video_file in processed_files:
            logging.info(f"File {video_file} already processed. Skipping.")
            continue

        start_time = progress.get(video_file, 0)
        print(f"start_time: {start_time}")
        process_video(video_file, start_time)
        print(f"Processed: {video_file}")

# 开始处理视频
process_files()

print("处理完成")
