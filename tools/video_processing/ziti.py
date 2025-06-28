import os
import subprocess

# 字体路径和 Fontconfig 配置路径
font_path = '/Windows/Fonts/segoepr.ttf'  # 示例系统中的字体路径
fontconfig_path = r'C:/font.conf'  # Fontconfig 配置文件路径

# 检查字体文件是否存在
#if not os.path.exists(font_path):
#    raise FileNotFoundError(f"The specified font file does not exist: {font_path}")

# 设置 Fontconfig 的配置文件路径为环境变量
os.environ['FONTCONFIG_FILE'] = fontconfig_path

# 使用 ffmpeg 检测字体是否可用
def check_font_usable(font_path):
    # 创建一个临时测试文件
    test_output = 'test_output.mp4'

    try:
        # 运行 ffmpeg 命令，测试能否使用字体绘制文本
        #cmd = [
        #    'ffmpeg', '-f', 'lavfi', '-i', 'color=size=320x240:rate=25:color=black',
        #    '-vf', f"drawtext=text='SleepyKitty':fontfile={font_path}:x=10:y=10:fontsize=24:fontcolor=white",
        #    '-t', '1', '-y', test_output
        #]
        cmd = [
            'ffmpeg','-loglevel','verbose','-f', 'lavfi', '-i', 'color=size=320x240:rate=25:color=black',
            '-vf', f"drawtext=text='SleepyKitty':font=youran:x=10:y=10:fontsize=24:fontcolor=white",
            '-t', '1', '-y', test_output
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"FFmpeg output: {result.stderr}")

        # 检查是否有错误
        if result.returncode == 0:
            print(f"Font {font_path} is usable.")
            return True
        else:
            print(f"Font {font_path} is not usable. FFmpeg output: {result.stderr}")
            return False
    finally:
        print("ok")
        # 删除临时文件
        #if os.path.exists(test_output):
        #    os.remove(test_output)


# 检查字体是否可用
if not check_font_usable(font_path):
    raise RuntimeError(f"Font {font_path} is not usable with ffmpeg.")
