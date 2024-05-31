## 绘制财富分布可视化图，数据来源：
# 中金财富报告2023的披露，中国总的私有财富是440万亿，93.76%的人口占据其中7%，人均2.2万，5.91%的人口占据其中25.6%，人均132万，0.33%的人口占据其中67.4%，人均6304万

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 数据# 设置字体为SimHei显示中文
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# 数据
total_wealth = 440e12  # 总的私有财富
wealth_distribution = [0.07, 0.256, 0.674]  # 各组所占的财富比值
population_distribution = [0.9376, 0.0591, 0.0033]  # 各组所占的人口比值

# 创建图形
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# 定义锥体参数
height = np.array(wealth_distribution)
radius = np.array(population_distribution)

# 颜色列表
colors = ["blue", "green", "red"]


# 创建圆锥形函数
def plot_cone(ax, height, radius, z_pos, color):
    # 创建锥体的顶点
    z = np.linspace(z_pos, z_pos + height, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * (1 - (z_grid - z_pos) / height) * np.cos(theta_grid)
    y_grid = radius * (1 - (z_grid - z_pos) / height) * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=0.6)


# 绘制三个圆锥
z_base = 0
for i in range(3):
    plot_cone(ax, height[i], radius[i], z_base, colors[i])
    z_base += height[i]
# 计算人均财富
average_wealth = [2.2, 132, 6304]  # 人均财富
print(average_wealth)
# 添加数据标签
labels = [
    f"财富占比7%，人口占比93.76%，人均财富{average_wealth[0]}万",
    f"财富占比26%，人口占比5.91%，人均财富{average_wealth[1]}万",
    f"财富占比67%，人口占比0.33%，人均财富{average_wealth[2]}万",
]
z_positions = [
    height[0] / 2,
    height[0] + height[1] / 2,
    height[0] + height[1] + height[2] / 2,
]
for i in range(3):
    ax.text(0, 0, z_positions[i], labels[i], color=colors[i], fontsize=10, ha="center")

# 设置坐标轴标签
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("财富分布")

# 设置视角
ax.view_init(elev=20, azim=30)

# 设置标题
plt.title("中国财富分布的3D锥形图")
plt.show()
