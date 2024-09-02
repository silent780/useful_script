from zhipuai import ZhipuAI

# 填写您自己的APIKey
client = ZhipuAI(api_key="")

# 存储所有生成的集数
chapters = []

for i in range(1, 21):
    # 构建每次请求的内容
    prompt = f"""编写一部1万字的玄幻小说，第{i}集，每集500字左右，集末提示下集内容，上下集要连贯。"""

    # 发送请求并获取响应
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    # 获取生成的内容
    chapter_content = response.choices[0].message

    # 保存生成的集数内容到列表
    chapters.append(chapter_content)

    # 输出当前生成的集数内容
    print(f"第{i}集内容:")
    print(chapter_content.content)
    print("\n" + "=" * 50 + "\n")

    # 将当前集内容保存到单独的txt文件中
    with open(f"chapter_{i}.txt", "w", encoding="utf-8") as file:
        file.write(chapter_content.content)
