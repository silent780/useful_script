import numpy as np
from scipy.linalg import eigh
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统使用黑体
plt.rcParams['axes.unicode_minus'] = False     
class SimpleVASP:
    def __init__(self, lattice_constant, atoms_positions):
        """
        初始化系统
        :param lattice_constant: 晶格常数
        :param atoms_positions: 原子位置列表
        """
        self.lattice_constant = np.array(lattice_constant)
        self.atoms_positions = np.array(atoms_positions)
        self.num_atoms = len(atoms_positions)
        
        
    def calculate_electron_density(self, grid_points=50):
        """
        计算简化的电子密度
        使用高斯函数模拟电子云
        """
        x = np.linspace(0, self.lattice_constant[0], grid_points)
        y = np.linspace(0, self.lattice_constant[1], grid_points)
        z = np.linspace(0, self.lattice_constant[2], grid_points)
        density = np.zeros((grid_points, grid_points, grid_points))
        
        # 使用meshgrid创建3D网格
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # 为每个原子添加高斯型电子密度
        for atom_pos in self.atoms_positions:
            r = np.sqrt((X-atom_pos[0])**2 + 
                       (Y-atom_pos[1])**2 + 
                       (Z-atom_pos[2])**2)
            density += np.exp(-r**2)
        
        return density, (x, y, z)
    
    def plot_electron_density(self, density, coords, iso_value=0.5):
        """
        绘制3D电子密度分布
        :param density: 3D密度数组
        :param coords: (x,y,z)坐标网格
        :param iso_value: 等值面的阈值
        """
        x, y, z = coords
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # 创建3D图形
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制等值面
        ax.scatter(X[density > iso_value], 
                Y[density > iso_value], 
                Z[density > iso_value],
                c=density[density > iso_value],
                cmap='viridis',
                alpha=0.5)
        
        # 设置标签
        ax.set_xlabel('X (Å)')
        ax.set_ylabel('Y (Å)')
        ax.set_zlabel('Z (Å)')
        ax.set_title('电子密度分布 (等值面)')
        
        # 添加颜色条
        cbar = plt.colorbar(ax.collections[0])
        cbar.set_label('电子密度 (任意单位)')
        
        # 设置视角
        ax.view_init(elev=30, azim=45)
        
        plt.show()

    def optimize_structure(self, steps=100):
        """
        3D结构优化
        使用简单的势能模型进行原子位置优化
        :return: 优化后的3D原子位置
        """
        optimized_positions = self.atoms_positions.copy()
        
        for _ in range(steps):
            forces = np.zeros_like(optimized_positions)
            
            # 计算原子间的3D斥力
            for i in range(self.num_atoms):
                for j in range(self.num_atoms):
                    if i != j:
                        # 3D位置差向量
                        diff = optimized_positions[i] - optimized_positions[j]
                        distance = np.linalg.norm(diff)
                        # 简单的3D斥力模型
                        force = diff / (distance**3 + 1e-6)  # 添加小量避免除零
                        forces[i] += force
            
            # 更新3D位置
            optimized_positions += 0.01 * forces
            
            # 确保原子位置在晶格范围内
            optimized_positions = np.clip(optimized_positions, 
                                        [0,0,0], 
                                        self.lattice_constant)
        
        return optimized_positions

    def molecular_dynamics(self, steps=1000, dt=0.001, temperature=300):
        """
        3D分子动力学模拟
        使用Velocity Verlet算法
        :param steps: 模拟步数
        :param dt: 时间步长
        :param temperature: 模拟温度(K)
        :return: 原子轨迹数组 shape=(steps, num_atoms, 3)
        """
        positions = self.atoms_positions.copy()
        # 根据温度初始化随机速度
        velocities = np.random.randn(self.num_atoms, 3) * np.sqrt(temperature/300)
        trajectories = []
        
        for _ in range(steps):
            # 计算3D力
            forces = np.zeros_like(positions)
            for i in range(self.num_atoms):
                for j in range(self.num_atoms):
                    if i != j:
                        diff = positions[i] - positions[j]
                        distance = np.linalg.norm(diff)
                        force = diff / (distance**3 + 1e-6)
                        forces[i] += force
            
            # Velocity Verlet积分
            velocities += forces * dt / 2
            positions += velocities * dt
            
            # 周期性边界条件
            positions = positions % self.lattice_constant
            
            # 第二次速度更新
            forces_new = np.zeros_like(positions)
            for i in range(self.num_atoms):
                for j in range(self.num_atoms):
                    if i != j:
                        diff = positions[i] - positions[j]
                        distance = np.linalg.norm(diff)
                        force = diff / (distance**3 + 1e-6)
                        forces_new[i] += force
            
            velocities += forces_new * dt / 2
            
            # 简单的温度控制
            current_temp = np.mean(np.sum(velocities**2, axis=1))
            scale = np.sqrt(temperature/300 / current_temp)
            velocities *= scale
            
            trajectories.append(positions.copy())
        
        return np.array(trajectories)
# 使用示例
if __name__ == "__main__":
    # 示例用法
    lattice = [5.0, 5.0, 5.0]
    positions = np.array([
        [1.0, 1.0, 1.0],
        [2.0, 2.0, 2.0],
        [3.0, 1.5, 2.5]
    ])
    vasp = SimpleVASP(lattice, positions)
    density, (x, y, z) = vasp.calculate_electron_density()
    density, coords = vasp.calculate_electron_density()
    vasp.plot_electron_density(density, coords)

    # 结构优化
    optimized_positions = vasp.optimize_structure()
    print("优化后的原子位置：")
    print(optimized_positions)
    
    # 分子动力学模拟
    trajectories = vasp.molecular_dynamics()
    print("分子动力学轨迹形状：", trajectories.shape)