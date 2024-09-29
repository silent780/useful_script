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
        self.k_center = self.init_k_center(Data, K_value)

    def filter(self, Threshold):
        """
        remove outliers

        """
        pass

    def normalize(self):
        pass

    def init_k_center(self, K_value):
        """init k center
        random choose k center
        if distance between center and data is smaller than threshold,
        then add data to the center
        """
        k_center = self.data.sample(n=K_value)

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


if __name__ == "__main__":
    data = pd.DataFrame([[1, 2], [3, 4], [5, 6], [7, 8]])
    kmeans = Kmeans(data, 2, 100)
    kmeans.fit()
    kmeans.report()
    kmeans.auto_keamns()
