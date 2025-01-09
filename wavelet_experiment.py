import numpy as np
import pywt  # 用于小波变换
import matplotlib.pyplot as plt

# ==================== 小波变换 ====================
# 生成信号
t = np.linspace(0, 1, 1000)  # 时间轴
true_signal = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 20 * t)  # 原始信号

# 添加高斯噪声
noise = np.random.normal(0, 0.5, size=t.shape)  # 均值为0，标准差为0.5的噪声
noisy_signal = true_signal + noise

# 绘制原始信号和含噪信号
plt.figure(figsize=(10, 6))
plt.plot(t, true_signal, label='Original Signal')
plt.plot(t, noisy_signal, label='Noisy Signal', alpha=0.7)
plt.legend()
plt.title("Original vs Noisy Signal")
plt.show()

# ==================== 选择小波基函数和分解层数 ====================
# 选择小波基函数和分解层数
wavelet = 'db4'  # Daubechies 4
level = 4  # 分解层数

# 进行小波分解
coeffs = pywt.wavedec(noisy_signal, wavelet, level=level)  # 返回分解系数


# =================确定阈值（可以根据具体问题调整）====================
def soft_threshold(data, threshold):
    return np.sign(data) * np.maximum(np.abs(data) - threshold, 0)

# 对细节系数进行阈值处理
threshold = 0.5  # 阈值大小，可以调整
coeffs_denoised = [coeffs[0]]  # 保留低频部分
coeffs_denoised += [soft_threshold(detail, threshold) for detail in coeffs[1:]]  # 处理高频部分

# ====================重构信号====================================
# 使用处理后的系数重构信号
denoised_signal = pywt.waverec(coeffs_denoised, wavelet)

# 绘制降噪后的信号
plt.figure(figsize=(10, 6))
plt.plot(t, noisy_signal, label='Noisy Signal', alpha=0.7)
plt.plot(t, true_signal, label='Original Signal', linestyle='dashed')
plt.plot(t, denoised_signal, label='Denoised Signal', linewidth=2)
plt.legend()
plt.title("Denoised Signal")
plt.show()

# ====================计算信噪比====================
# 计算信噪比
mse = np.mean((true_signal - denoised_signal) ** 2)
snr = 10 * np.log10(np.mean(true_signal ** 2) / mse)
print(f"SNR: {snr:.2f} dB")

