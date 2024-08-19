"""
@File    :   RSM_exp.py
@Time    :   2024/08/19 16:53:58
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   响应曲面模型（Response Surface Model）是一种用于优化多变量系统的统计建模技术。
            它通过拟合实验数据的二次多项式模型来预测系统的响应，并使用优化算法来找到最佳的操作条件。
            这个示例演示了如何使用Python的statsmodels库和SciPy库来拟合响应曲面模型，
            并使用优化算法来找到最佳操作条件。
"""

# here put the import lib

import numpy as np
from pyDOE import ccdesign
from scipy.optimize import minimize
import statsmodels.api as sm
from statsmodels.formula.api import ols
import pandas as pd

# 生成中心复合设计（2个因素）
design = ccdesign(2, center=(4, 4))

# 设置中心点的具体值（例如：温度范围 50-100，时间范围 10-50）
design[:, 0] = design[:, 0] * 25 + 75  # 温度
design[:, 1] = design[:, 1] * 20 + 30  # 时间

# 假设实验结果
responses = np.array([85, 88, 90, 87, 84, 92, 89, 91, 93, 85, 87, 88, 90])

# 创建数据表
data = pd.DataFrame(design, columns=["temperature", "time"])
data["response"] = responses

# 拟合二次多项式模型
model = ols(
    "response ~ temperature + time + I(temperature**2) + I(time**2) + temperature:time",
    data=data,
).fit()


# 预测和优化（例如使用SciPy的optimize模块）
def response_function(x):
    return -(
        model.params["Intercept"]
        + model.params["temperature"] * x[0]
        + model.params["time"] * x[1]
        + model.params["I(temperature ** 2)"] * x[0] ** 2
        + model.params["I(time ** 2)"] * x[1] ** 2
        + model.params["temperature:time"] * x[0] * x[1]
    )


# 初始猜测
initial_guess = [75, 30]

# 寻找最优值
result = minimize(response_function, initial_guess, bounds=[(50, 100), (10, 50)])
optimal_conditions = result.x

print(
    "最佳条件：温度 = {:.2f}, 时间 = {:.2f}".format(
        optimal_conditions[0], optimal_conditions[1]
    )
)

# 运筹优化部分示例（假设有生产资源的限制，如原材料和人力）
from scipy.optimize import linprog

# 目标函数系数（假设成本最小化问题）
c = [10, 15]  # 原材料和人力的单位成本

# 不等式约束矩阵和向量（假设一些资源限制）
A = [[1, 2], [2, 1]]
b = [100, 80]

# 变量非负约束
x_bounds = (0, None)
bounds = [x_bounds, x_bounds]

# 使用线性规划进行优化
result_lp = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

print("资源分配：原材料 = {:.2f}, 人力 = {:.2f}".format(result_lp.x[0], result_lp.x[1]))
