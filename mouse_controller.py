"""
@File    :   mouse_controller.py
@Time    :   2024/08/19 16:46:03
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   None
"""

# here put the import lib

from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller


mouse = Controller()


def on_press(key):
    # 当按下esc，结束监听
    if key == Key.esc:
        print(f"你按下了 esc，监听结束")
        return False
    print(f"你按下了 {key} 键")


def on_release(key):
    print(f"你松开了 {key}键")


if __name__ == "__main__":

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
