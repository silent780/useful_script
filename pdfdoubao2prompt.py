import os
import fitz
import base64
from openai import OpenAI
import pandas as pd
from PIL import Image
import io
import re
import time

INPUT_ROOT = r"C:\Users\49498\Desktop\素材"
OUTPUT_EXCEL = "test_output_results.xlsx"
IMAGE_QUALITY = 90
MAX_RETRIES = 3

# 修改配置部分
API_KEY = "1"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"  # 更新为新的API地址

# 初始化客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
def encode_image(image_path):
    """将图片转换为 base64 编码"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def call_doubao_api(image_path):
    """使用 OpenAI SDK 调用 API"""
    base64_image = encode_image(image_path)
    
    for _ in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="doubao-1-5-vision-pro-32k-250115",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": "请提取这张图片中的5个关键词，用逗号分隔"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            # 处理响应
            if response.choices:
                content = response.choices[0].message.content
                # 分割关键词并清理空白
                keywords = [word.strip() for word in content.split(',')]
                # 只返回前5个关键词
                return keywords[:5]
                
        except Exception as e:
            print(f"API调用失败: {str(e)}")
            # time.sleep(2)  # 失败后等待2秒再重试
            
    return []  # 如果所有重试都失败，返回空列表
def encode_image(image_path):
    """将图片转换为 base64 编码"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def sanitize_filename(name):
    """清理文件名中的特殊字符"""
    return re.sub(r'[\\/*?:"<>|]', "", name[:20])

def pdf_to_images(pdf_path, output_dir, parent_folder, pdf_name):
    """将PDF转换为JPG图像"""
    doc = fitz.open(pdf_path)
    pdf_short = sanitize_filename(pdf_name.replace(".pdf", ""))
    
    images = []
    for pg in range(doc.page_count):
        page = doc.load_page(pg)
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))
        
        # 生成文件名
        img_name = f"{parent_folder}_{pdf_short}_p{pg+1:03d}.jpg"
        img_path = os.path.join(output_dir, img_name)
        img.save(img_path, "JPEG", quality=IMAGE_QUALITY)
        images.append(img_path)
    return images


def process_all_files():
    """主处理流程"""
    all_results = []
    
    # 遍历根目录
    for root, dirs, files in os.walk(INPUT_ROOT):
        parent_folder = os.path.basename(root)
        
        # 跳过根目录
        if root == INPUT_ROOT:
            continue
            
        # 创建临时图片目录
        temp_img_dir = os.path.join(root, "_temp_images")
        os.makedirs(temp_img_dir, exist_ok=True)
        
        # 处理每个PDF
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                
                try:
                    # 转换PDF为图片
                    images = pdf_to_images(pdf_path, temp_img_dir, parent_folder, file)
                    
                    # 处理每张图片
                    for img_path in images:
                        keywords = call_doubao_api(img_path)
                        
                        if len(keywords) >= 5:
                            record = {
                                "文件夹名": parent_folder,
                                "图片名称": os.path.basename(img_path),
                                "关键词1": keywords[0],
                                "关键词2": keywords[1],
                                "关键词3": keywords[2],
                                "关键词4": keywords[3],
                                "关键词5": keywords[4]
                            }
                            all_results.append(record)
                            print(keywords)
                        break
                except Exception as e:
                    print(f"处理文件失败: {pdf_path} - {str(e)}")
                    break
    
    # 生成Excel报告
    if all_results:
        df = pd.DataFrame(all_results)
        df.to_excel(OUTPUT_EXCEL, index=False)
        print(f"处理完成！结果已保存至：{OUTPUT_EXCEL}")
    else:
        print("未找到可处理的有效文件")

if __name__ == "__main__":
    # 生成Excel报告
    all_results = {"key": "value"}
    if all_results:
        df = pd.Series(all_results)
        df.to_excel(OUTPUT_EXCEL, index=False)
        print(f"处理完成！结果已保存至：{OUTPUT_EXCEL}")
    else:
        print("未找到可处理的有效文件")