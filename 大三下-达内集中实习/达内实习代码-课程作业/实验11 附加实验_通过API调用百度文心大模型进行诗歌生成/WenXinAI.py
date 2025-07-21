import requests
import json

def call_wenxin_api(api_key, model_id, topic, length=200, style="抒情", sentiment=0.5, temperature=0.7, genre="诗"):
    """调用文心大模型API，生成中文诗歌"""
    # 构造请求参数
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    sentiment_desc = "积极" if sentiment > 0 else "消极" if sentiment < 0 else "中立"
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": f"请以'{topic}'为主题，生成一篇长度约为{length}字的{genre}，风格为{style}，情感基调为{sentiment_desc}。"
            }
        ],
        "temperature": temperature,
        "stream": False
    }

    # 发送请求并处理响应
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 检查HTTP请求是否成功
        result = response.json()

        # 检查是否存在'result'字段
        if "result" in result:
            return result["result"]
        elif "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
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
    API_KEY = "#"  # 替换为你的API密钥
    MODEL_ID = "ERNIE X1 Turbo"  # 模型ID，可根据实际情况调整
    TOPIC = "秋天"  # 诗歌主题
    LENGTH = 100  # 生成长度
    STYLE = "浪漫主义、家国情怀"  # 诗歌风格
    SENTIMENT = -0.5  # 情感基调，-1为消极，1为积极
    TEMPERATURE = 0.7  # 温度参数
    GENRE = "宋词"  # 文学体裁

    # 2. 调用API并打印结果
    poem = call_wenxin_api(API_KEY, MODEL_ID, TOPIC, LENGTH, STYLE, SENTIMENT, TEMPERATURE, GENRE)
    print("生成的诗歌：")
    print(poem)