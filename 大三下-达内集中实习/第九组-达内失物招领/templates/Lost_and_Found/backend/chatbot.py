import requests

# 假设的常量定义
MODEL_ID_5 = "ernie-3.5-8k"  # 需要替换为实际的模型ID
API_KEY_5 = "bce-v3/ALTAK-tsnLC0fnoYPFgDYYOt4JA/4562efa9721ae31061204235412613e7879397a2"
CHAT_URL_5 = "https://qianfan.baidubce.com/v2/chat/completions"

class QianfanChat:
    def __init__(self, access_token):
        self.access_token = access_token
        self.chat_history = []  # 保存多轮对话历史

    def call_model(self, user_input):
        """调用大模型，返回回复"""
        # 检查Access Token是否为空
        if not self.access_token:
            return "错误：Access Token不能为空"

        # 添加最新用户输入到对话历史
        self.chat_history.append({"role": "user", "content": user_input})
        # 限制历史长度（避免超过模型输入限制，保留最近10轮）
        if len(self.chat_history) > 20:
            self.chat_history = self.chat_history[-20:]

        # 构建请求头（核心：用Access Token认证）
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"  # 关键：Bearer + Access Token
        }

        # 构建请求参数
        payload = {
            "model": MODEL_ID_5,
            "messages": self.chat_history,
            "temperature": 0.7,  # 回复随机性
            "stream": False  # 非流式返回
        }

        try:
            # 发送POST请求
            response = requests.post(
                url=CHAT_URL_5,
                headers=headers,
                json=payload,  # 直接传json参数（自动序列化）
                timeout=30
            )
            response.raise_for_status()  # 抛出HTTP错误（如401、403）
            result = response.json()

            # 解析回复
            if "choices" in result and len(result["choices"]) > 0:
                assistant_reply = result["choices"][0]["message"]["content"]
                self.chat_history.append({"role": "assistant", "content": assistant_reply})
                return assistant_reply
            else:
                return f"模型返回异常：{result.get('error', '未知错误')}"

        except requests.exceptions.HTTPError as e:
            # 处理HTTP错误（如Token过期、权限不足）
            if response.status_code == 401:
                return "错误：Access Token无效或已过期，请重新生成"
            elif response.status_code == 403:
                return "错误：没有调用该模型的权限，请在控制台开通"
            else:
                return f"HTTP错误：{str(e)}"
        except Exception as e:
            return f"调用失败：{str(e)}"