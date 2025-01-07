import pygame
import time
import sys
from pygame import mixer

class RainPlayer:
    def __init__(self):
        """初始化播放器"""
        pygame.init()
        mixer.init()
        self.playing = False
        self.volume = 1.0

    def load(self, file_path: str):
        """加载音频文件"""
        try:
            mixer.music.load(file_path)
            print(f"已加载音频: {file_path}")
            return True
        except Exception as e:
            print(f"加载失败: {e}")
            return False

    def play(self):
        """开始播放"""
        if not self.playing:
            mixer.music.play(-1)  # -1表示无限循环
            mixer.music.set_volume(self.volume)
            self.playing = True
            print("开始播放")

    def stop(self):
        """停止播放"""
        if self.playing:
            mixer.music.stop()
            self.playing = False
            print("停止播放")

    def set_volume(self, volume: float):
        """设置音量 (0.0 到 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        mixer.music.set_volume(self.volume)
        print(f"音量设置为: {self.volume}")

    def quit(self):
        """退出播放器"""
        self.stop()
        pygame.quit()

def main():
    player = RainPlayer()
    
    # 加载音频文件
    if not player.load(r"data\obj_wo3DlMOGwrbDjj7DisKw_28587931939_2e2e_9ea6_7c53_8a14881172a5a360ce39e572df964fc2.mp3"):  # 替换为你的雨声文件路径
        return

    try:
        player.play()
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n正在退出...")
        player.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()