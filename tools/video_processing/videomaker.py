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
output_folder = r'/volume2/Download/sucai/sleepykitty'
record_file = 'processed_files.txt'  # 记录处理过的视频文件

# 创建或读取记录文件，确保UTF-8编码
if not os.path.exists(record_file):
    open(record_file, 'w', encoding='utf-8').close()

# 读取已处理文件列表
with open(record_file, 'r', encoding='utf-8') as f:
    processed_files = set(line.strip() for line in f)

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

# 修改视频元数据和文件名
def rename_and_update_metadata(input_file, new_file_name, new_metadata_title):
    try:
        cmd = [
            'ffmpeg', '-i', input_file, '-c', 'copy',
            '-metadata', f'title={new_metadata_title}', new_file_name
        ]
        subprocess.run(cmd)
        logging.info(f"Updated metadata and renamed: {input_file} -> {new_file_name}")
    except Exception as e:
        logging.error(f"Error updating metadata: {e}")

# 处理视频
def process_video(input_file):
    try:
        # 为临时文件生成唯一的时间戳后缀
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        #temp_video = f'temp_{timestamp}.mp4'
        #cmd = ['ffmpeg', '-i', input_file, '-ss', '0', '-to', '35940', '-c', 'copy', temp_video]
        #subprocess.run(cmd)

        #fade_in = f'fadein_{timestamp}.mp4'
        #cmd = ['ffmpeg', '-i', temp_video, '-vf', 'fade=t=in:st=0:d=5', fade_in]
        #subprocess.run(cmd)

        #watermarked = f'watermarked_{timestamp}.mp4'
        #cmd = ['ffmpeg', '-i', fade_in, '-vf',
        #       f"drawtext=text='{watermark_text}':fontfile={font_path}:x=10:y=10:fontsize=48:fontcolor=white@0.5", watermarked]
        #subprocess.run(cmd)

        audio1 = bgm_path
        audio2 = get_random_audio_file(audio_folder)

        # 创建输出文件夹和文件名
        output_subfolder, now = create_output_folder()
        final_output = os.path.join(output_subfolder, f"{now}p.mp4")
        new_metadata_title = f"{now}p"

        # 合成视频和音频
        #cmd = [
        #    'ffmpeg','-y', '-i', watermarked,
        #    '-i', audio1, '-i', audio2,
        #    '-filter_complex',
        #    f"[1:a]aloop=loop=-1:size=2e+09[a1];[2:a]aloop=loop=-1:size=2e+09[a2];"
        #    f"[a1]volume=0.8[a1v];[a1v][a2]amerge=inputs=2[a]",
        #    '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-b:v', '3000k', '-c:a', 'aac',
        #    '-shortest', '-r', '30', '-metadata', f'title={new_metadata_title}', final_output
        #]
        #subprocess.run(cmd)

        cmd = [
            'ffmpeg', '-y', '-i', input_file, '-i', audio1, '-i', audio2,
            '-vf', f"fade=t=in:st=0:d=5, drawtext=text='{watermark_text}':fontfile={font_path}:x=10:y=10:fontsize=48:fontcolor=white@0.5",
            '-filter_complex', 
            f"[1:a]aloop=loop=-1:size=2e+09[a1]; [2:a]aloop=loop=-1:size=2e+09[a2]; [a1]volume=0.7[a1v]; [a1v][a2]amerge=inputs=2[a]",
            '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-b:v', '3000k', '-c:a', 'aac', '-shortest', '-r', '30',
            '-ss', '0', '-to', '35940', '-metadata', f'title={new_metadata_title}', final_output
        ]
        subprocess.run(cmd)
        
        # 删除临时文件
        #os.remove(temp_video)
        #os.remove(fade_in)
        #os.remove(watermarked)

        with open(record_file, 'a', encoding='utf-8') as f:
            f.write(input_file + '\n')

        logging.info(f"Processed video: {input_file}")

    except Exception as e:
        logging.error(f"Error processing video: {input_file}, Error: {e}")

# 创建输出文件夹和文件名
def create_output_folder():
    now = datetime.now().strftime("%m%d%H%M")
    output_subfolder = os.path.join(output_folder, f"{now}p")
    os.makedirs(output_subfolder, exist_ok=True)
    logging.info(f"Created output folder: {output_subfolder}")
    return output_subfolder, now

# 处理所有视频文件
def process_files():
    mp4_files = sorted(get_mp4_files(video_folder))
    for video_file in mp4_files:
        if video_file in processed_files:
            logging.info(f"File {video_file} already processed. Skipping.")
            continue

        process_video(video_file)
        print(f"Processed: {video_file}")

# 开始处理视频
process_files()

print("处理完成")
