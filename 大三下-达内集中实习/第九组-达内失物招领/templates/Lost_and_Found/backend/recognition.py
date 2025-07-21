import requests
import json
import base64

def local_image_to_base64(image_path):
    """将本地图片转换为带格式前缀的Base64字符串"""
    # 从路径提取图片格式（如"test.jpg" → "jpg"）
    image_format = image_path.split(".")[-1].lower()
    allowed_formats = ["jpg", "jpeg", "png", "gif", "bmp","webp"]  # API支持的格式
    if image_format not in allowed_formats:
        raise ValueError(f"不支持的图片格式：{image_format}，仅支持{allowed_formats}")

    # 读取本地图片并转换为Base64
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()  # 读取二进制内容
            base64_str = base64.b64encode(image_bytes).decode("utf-8")  # 编码为字符串
    except FileNotFoundError:
        raise FileNotFoundError(f"图片路径不存在：{image_path}")
    except Exception as e:
        raise Exception(f"读取图片失败：{str(e)}")

    # 拼接API要求的格式前缀（必须包含，否则无法识别）
    return f"data:image/{image_format};base64,{base64_str}"


def call_qianfan_api(api_key, model_id, image_path, prompt="描述这张图片的内容"):
    """调用千帆API，使用本地图片获取描述结果"""
    # 1. 转换本地图片为Base64
    try:
        base64_image = local_image_to_base64(image_path)
    except Exception as e:
        return f"图片处理错误：{str(e)}"

    # 2. 构造请求参数
    url = "https://qianfan.baidubce.com/v2/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"  # 鉴权格式：Bearer + 空格 + API Key
    }
    payload = {
        "model": model_id,  # 模型ID（如deepseek-vl2，需替换为实际使用的模型）
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},  # 用户指令（可自定义）
                    {"type": "image_url", "image_url": {"url": base64_image}}  # 本地图片的Base64
                ]
            }
        ],
        "stream": False  # 非流式返回（一次获取完整结果）
    }

    # 3. 发送请求并处理响应
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 检查HTTP请求是否成功（如404、500等错误）
        result = response.json()

        # 4. 解析响应结果
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]  # 返回图片描述结果
        else:
            return f"API返回异常：{json.dumps(result, ensure_ascii=False)}"

    except requests.exceptions.RequestException as e:
        return f"请求失败：{str(e)}"
    except json.JSONDecodeError:
        return "API返回结果解析失败（非JSON格式）"


# --------------------------
# 以下为使用示例（需替换为你的信息）
# --------------------------
if __name__ == "__main__":
    # 1. 替换为你的实际信息
    API_KEY = "bce-v3/ALTAK-5cMwyb1C4wg8YoEcaqeNh/f1f4f623745db09677a08f27fcd24f0dcf75a18f"  # 例如："bce-v3/ALTAKxxxxxxxxxxxxxxxxxxxx"
    MODEL_ID = "deepseek-vl2"  # 视觉模型ID（可替换为其他支持的模型）
    IMAGE_PATH = "D:/python/失物招领/2.webp"  # 例如："./test.png" 或 "C:/images/photo.jpg"
    PROMPT = "详细描述这张图片的内容，包括物体、场景和颜色"  # 自定义指令

    # 2. 调用API并打印结果
    description = call_qianfan_api(API_KEY, MODEL_ID, IMAGE_PATH, PROMPT)
    print("图片描述结果：")
    print(description)