# here put the import lib

import pandas as pd
import ydata_profiling
import numpy as np

# # 设置采样率和周期
# sampling_rate = 100
# frequency = 5

# # 计算时间序列的长度
# T = 2.0 / frequency
# num_samples = int(sampling_rate * T)

# # 生成时间序列
# t = np.linspace(0, T, num_samples, endpoint=False)
# x = np.sin(2 * np.pi * frequency * t)

# # 将时间序列存入字典中
# data = {'Time': t, 'Amplitude': x}

# # 将字典转换为DataFrame类型
# df = pd.DataFrame(data)

# # 将Time列设置为时间序列类型
# df['Time'] = pd.to_datetime(df['Time'], unit='s')
# df.set_index('Time', inplace=True)

# # 生成报告


def ts_profiling(df: pd.DataFrame, output_file: str = "profiling_report.html") -> None:
    profile = ydata_profiling.ProfileReport(df, tsmode=True)
    profile.to_file(output_file)
