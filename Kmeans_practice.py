"""
@File    :   Kmeans_practice.py
@Time    :   2024/09/29 10:39:34
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   Try to build a kmeans algorithm
"""

# here put the import lib
import pandas as pd


class Sample_point:
    """
    sample point
    """

    def __init__(self, k_center: None | pd.DataFrame = None, **kwargs) -> None:
        self.k_center = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def compute_distance(self, sample_data):
        """compute the distance between sample data and k center"""


class Kmeans:
    """build a simple kmeans algorithm
    input: data: pd.DataFrame
    output: k_center: pd.DataFrame

    basic work flow:
        filter: remove outliers
        normalize: normalize data
        init_k_center: init k center
        distance: calculate the distance between sample data and k center
        update_k_center: update k center
        predict: input a sample data and output the nearest k center

    auto_k_means: auto find the best k value

    example:
        data = pd.DataFrame([[1, 2], [3, 4], [5, 6], [7, 8]])
        kmeans = Kmeans(data, 2, 100)
        kmeans.fit()
        kmeans.report()
        kmeans.auto_keamns()

    methods:
        filter: remove outliers
        normalize: normalize data
        init_k_center: init k center
        distance: calculate the distance between sample data and k center
        update_k_center: update k center
        predict: input a sample data and output the nearest k center
        fit: fit the data
        report: report the result
        auto_keamns: auto find the best k value


    """

    def __init__(self, Data, K_value, Max_iterations) -> None:
        self.data = pd.DataFrame(Data)
        self.k = K_value
        self.Max_iterations = Max_iterations
        self.k_center = self.init_k_center()

    def filter(self, Threshold):
        """
        remove outliers

        """
        pass

    def normalize(self):
        """normalize data"""
        self.data = (self.data - self.data.mean()) / self.data.std()
        print(self.data.head())

    def init_k_center(self):
        """init k center
        random choose k center
        if distance between center and data is smaller than threshold,
        then add data to the center
        """
        k_center = self.data.sample(n=self.k)

        return k_center

    def distance(self, sample_data, k_center):
        """calculate the distance between sample data and k center"""
        distance = []
        for i in range(self.k):
            distance.append(
                (
                    (sample_data[0] - k_center[i][0]) ** 2
                    + (sample_data[1] - k_center[i][1]) ** 2
                )
                ** 0.5
            )
        return distance

    def update_k_center(self, x, y):
        pass

    def predict(self, sample_data):
        """input a sample data and output the nearest k center"""
        sample_data = pd.DataFrame(sample_data)
        k_center = self.k_center
        distance = self.distance(sample_data, k_center)
        k_center = self.update_k_center(sample_data, distance)

        return k_center

    def find_nearest_k_center(self, x, y):
        pass

    def fit(self):
        pass

    def report(self):
        pass

    def auto_keamns(self):
        pass


def build_example(sample_num: int = 10000):
    import torch
    import matplotlib.pyplot as plt

    n_data = torch.ones(sample_num, 2)
    xy0 = torch.normal(
        2 * n_data, 1
    )  # 生成均值为2，2 标准差为1的随机数组成的矩阵 shape=(sample_num, 2)
    c0 = torch.zeros(sample_num)
    xy1 = torch.normal(
        -2 * n_data, 1
    )  # 生成均值为-2，-2 标准差为1的随机数组成的矩阵 shape=(sample_num, 2)
    c1 = torch.ones(sample_num)
    X = torch.cat((xy0, xy1), 0)
    c = torch.cat((c0, c1), 0)

    plt.scatter(
        X[:, 0],
        X[:, 1],
        c=c,
        s=10,
        cmap="RdYlGn",
        alpha=0.7,
    )  # 在这个 plt.scatter 函数中，cmap 参数指定了颜色渐变的模式。 "RdYlGn" 是一个预定义的 colormap 名称，表示从红色（Red）到黄色（Yellow）到绿色（Green）的渐变。

    plt.xlabel("x")
    plt.show()
    print(X.shape)
    return X


if __name__ == "__main__":
    data = build_example(100)
    # data = pd.DataFrame([[1, 2], [3, 4], [5, 6], [7, 8]])

    kmeans = Kmeans(data, 2, 100)
    kmeans.normalize()
    print(kmeans.init_k_center())
