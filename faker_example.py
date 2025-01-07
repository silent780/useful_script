from faker import Faker, finance

# 设置 Faker 语言版本为中文
fake = Faker("zh_CN")

print(fake.name())  # 生成姓名
print(fake.address())  # 生成地址
print(fake.email())
print(finance.accountName())  # 生成金融相关的数据
