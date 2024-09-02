import numpy as np
import pandas as pd

standerd_bmi = [18.5, 24.5]
activate_level_dict = {"lay_down": 25, "low": 30, "medium": 35, "high": 40}  # kcal/kg
nutrition_scale_dict = {"protein": 0.15, "fat": 0.3, "carbohydrate": 0.55}  # rate
nutrition_energe_dict = {"protein": 4, "fat": 9, "carbohydrate": 4}  # kcal/g

# food_nutritions = pd.read_csv("food_nutritions.csv")


class Food_Recommendation:
    def __init__(self, AimDiet_Calculator) -> None:
        self.AimDiet_Calculator = AimDiet_Calculator

    def get_food_nutritions(self):
        pass

    def Solver(self):
        pass

    def get_food_recommendation(self):
        """ """
        recommend_nutritions = self.AimDiet_Calculator.nutrition_calculator()
        food_nutritions = self.get_food_nutritions()
        solver = self.Solver()
        pass


class AimDiet_Calculator:
    def __init__(
        self, weight, height, age, sex, name="someone", activate_level: str = "medium"
    ) -> None:
        self.name = name
        self.weight = weight
        self.height = height
        self.age = age
        self.sex = sex
        self.bmi = self.get_bmi()
        self.activate_level = activate_level
        self.aim_weight = self.get_norm_weight()
        self.aim_calories = self.get_norm_calories()
        self.standerd_bmi = standerd_bmi
        self.activate_level_dict = activate_level_dict
        self.nutrition_scale_dict = nutrition_scale_dict
        self.nutrition_energe_dict = nutrition_energe_dict

    def get_norm_weight(self):
        """return the normal weight of a person given their height and weight"""
        return self.height - 105

    def get_BMR(self):
        """return the basal metabolic rate of a person given their weight, height
        and age"""
        if self.sex == "male":
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

    def get_norm_calories(self):
        norm_weight = self.get_norm_weight()
        return norm_weight * activate_level_dict[self.activate_level]

    def nutrition_calculator(self):
        """return the quantity of protein, fat, and carbohydrate that a person should consume given their weight and height"""
        norm_calories = self.get_norm_calories()
        return {
            key: round((norm_calories * value / nutrition_energe_dict[key]), 2)
            for key, value in nutrition_scale_dict.items()
        }

    def get_bmi(self):
        """return the body mass index of a person given their height and weight"""
        return round(self.weight / (self.height / 100) ** 2, 2)

    def get_weight_suggestion(self):
        """return the suggested weight of a person given their height"""
        aim_weight = self.get_norm_weight()
        lowest_bmi, highest_bmi = self.standerd_bmi
        lowest_weight = round(lowest_bmi * (self.height / 100) ** 2, 2)
        highest_weight = round(highest_bmi * (self.height / 100) ** 2, 2)
        if self.weight < lowest_weight:
            suggestion = f"增重 {lowest_weight - self.weight} kg"
        elif self.weight > highest_weight:
            suggestion = f"减重 {self.weight - highest_weight} kg"
        else:
            suggestion = f"保持当前体重,但最好达到 {aim_weight} kg"
        return f"标准体重: {aim_weight}, 最低体重: {lowest_weight}, 最高体重: {highest_weight} 你应该 {suggestion}"

    def report(self):
        return {
            "姓名": self.name,
            "体重": self.weight,
            "身高": self.height,
            "年龄": self.age,
            "蛋白质摄入": self.nutrition_calculator()["protein"],
            "脂肪摄入": self.nutrition_calculator()["fat"],
            "碳水摄入": self.nutrition_calculator()["carbohydrate"],
            "bmi": self.get_bmi(),
            "标准体重": self.aim_weight,
            "标准摄入热量": self.aim_calories,
            "基础代谢": calculator.get_BMR(),
            "体重建议": self.get_weight_suggestion(),
        }


if __name__ == "__main__":

    calculator_glx = AimDiet_Calculator(
        name="glx", weight=78, height=178, age=29, sex="male", activate_level="low"
    )
    calculator_crs = AimDiet_Calculator(
        name="crs", weight=48, height=159, sex="female", age=29, activate_level="low"
    )

    for calculator in [calculator_glx, calculator_crs]:
        print(calculator.name.center(50, "="))
        # print(calculator.get_norm_calories())
        # print(calculator.nutrition_calculator())
        # print(calculator.get_weight_suggestion())
        # print(f"基础代谢: {calculator.get_BMR()}" + "\n")
        print(calculator.report())
