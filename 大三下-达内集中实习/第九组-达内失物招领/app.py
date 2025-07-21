# 导入必要的库
from flask import Flask, request, jsonify, send_from_directory, render_template, abort
from flask import redirect, flash, url_for  # Flask核心库及请求、响应处理工具
from flask_sqlalchemy import SQLAlchemy  # 数据库ORM工具
from flask_cors import CORS  # 跨域资源共享支持
import os  # 文件系统操作
import uuid  # 生成唯一ID
import datetime  # 日期时间处理
from werkzeug.security import generate_password_hash

# 初始化Flask应用
app = Flask(__name__)  # 指定模板文件夹路径
# 启用CORS，解决前后端跨域问题
CORS(app)

# -------------------------- 应用配置（MySQL版本） --------------------------
# MySQL数据库配置
# 格式：mysql+pymysql://用户名:密码@主机地址:端口号/数据库名?charset=utf8mb4
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/lost_and_found?charset=utf8mb4'
# 禁用SQLAlchemy的修改跟踪功能，提高性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 配置文件上传目录
app.config['UPLOAD_FOLDER'] = 'uploads'
# 限制上传文件大小为5MB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# 创建上传文件夹（如果不存在）
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化数据库实例
db = SQLAlchemy(app)


# -------------------------- 数据库模型设计（适配MySQL） --------------------------
# 失物信息模型
class LostItem(db.Model):
    __tablename__ = 'lost_items'  # MySQL建议显式指定表名
    id = db.Column(db.String(36), primary_key=True)  # 物品唯一ID
    user_id = db.Column(db.String(36), nullable=False)  # 发布用户ID
    item_type = db.Column(db.String(50), nullable=False)  # 物品类型
    name = db.Column(db.String(100), nullable=False)  # 物品名称
    description = db.Column(db.Text, nullable=False)  # 物品描述
    lost_date = db.Column(db.Date, nullable=False)  # 丢失日期
    lost_location = db.Column(db.String(200), nullable=False)  # 丢失地点
    contact_name = db.Column(db.String(50), nullable=False)  # 联系人姓名
    contact_phone = db.Column(db.String(20), nullable=False)  # 联系电话
    image_url = db.Column(db.String(200))  # 物品图片URL
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # 创建时间
    status = db.Column(db.String(20), default='pending')  # 状态：待审核/已匹配/已找回


# 拾物（寻物）信息模型
class FoundItem(db.Model):
    __tablename__ = 'found_items'
    id = db.Column(db.String(36), primary_key=True)  # 物品唯一ID
    user_id = db.Column(db.String(36), nullable=False)  # 发布用户ID
    item_type = db.Column(db.String(50), nullable=False)  # 物品类型
    name = db.Column(db.String(100), nullable=False)  # 物品名称
    description = db.Column(db.Text, nullable=False)  # 物品描述
    found_date = db.Column(db.Date, nullable=False)  # 拾获 日期
    found_location = db.Column(db.String(200), nullable=False)  # 拾获地点
    storage_option = db.Column(db.String(50), nullable=False)  # 存放方式
    contact_name = db.Column(db.String(50), nullable=False)  # 联系人姓名
    contact_phone = db.Column(db.String(20), nullable=False)  # 联系电话
    image_url = db.Column(db.String(200))  # 物品图片URL
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # 创建时间
    status = db.Column(db.String(20), default='pending')  # 状态：待审核/已匹配/已认领

# 用户模型（修正表名和字段）
class LandF_User(db.Model):
    __tablename__ = 'LandF_users'  # 修正表名，避免与其他表冲突
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # 添加唯一性约束
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))  # 修正字段名（原Sex重复且不规范）
    birth = db.Column(db.Date)  # 修正为日期类型（原String不规范）
    age = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))  # 添加密码哈希字段

    # 添加密码设置方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


# 创建数据库表（应用启动时自动创建）
with app.app_context():
    db.create_all()

# -------------------------- 工具函数 与 后端调用--------------------------
def generate_uuid():
    """生成唯一UUID作为物品ID或匹配记录ID"""
    return str(uuid.uuid4())

# 付天乐-后端2
from templates.Lost_and_Found.backend.recognition import call_qianfan_api
API_KEY_2 = "bce-v3/ALTAK-5cMwyb1C4wg8YoEcaqeNh/f1f4f623745db09677a08f27fcd24f0dcf75a18f"
MODEL_ID_2 = "deepseek-vl2" # deepseek容易报错，替换模型为
PROMPT_2 = "详细描述这张图片的内容，包括物体、场景和颜色"

# 章子铉-后端3

# 李易珅-后端4

# 刘宇扬-后端5
from templates.Lost_and_Found.backend.chatbot import QianfanChat
MODEL_ID_5 = "ernie-3.5-8k"  # 需要替换为实际的模型ID
API_KEY_5 = "bce-v3/ALTAK-tsnLC0fnoYPFgDYYOt4JA/4562efa9721ae31061204235412613e7879397a2"
CHAT_URL_5 = "https://qianfan.baidubce.com/v2/chat/completions"
# -------------------------- 0. 前端页面 --------------------------

# 首页
@app.route("/")
def index():
    try:
        users = LandF_User.query.all()
        username = request.args.get('username')
        user_now = LandF_User.query.filter_by(username=username).first()
        return render_template('index.html', users=users, user_now=user_now)
    except Exception as e:
        print(f"数据库连接错误: {e}")
        return render_template('index.html', users=[], user_now=None)

# 登录
@app.route("/login", methods=['GET', 'POST'])
def login():
    return "登录"

@app.route('/logout')
def logout():
    username = request.args.get('username')
    flash('已成功退出登录', 'success')
    return redirect(url_for('index'))

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    return "注册"

@app.route('/recommendations')
def recommendations():
    # 这里可以添加具体的逻辑
    return "课程推荐页面"

# 首页路由
@app.route("/Lost_and_Found", methods=['GET', 'POST'])
def Lost_and_Found_index():
    return render_template('Lost_and_Found/Lost-and-Found-index.html')

# 失物发布路由
@app.route("/Lost_and_Found/lost-post", methods=['GET', 'POST'])
def lost_post():
    return render_template('Lost_and_Found/lost-post.html')

# 拾物发布路由
@app.route("/Lost_and_Found/found-post", methods=['GET', 'POST'])
def found_post():
    return render_template('Lost_and_Found/found-post.html')

# 通知中心路由
@app.route("/Lost_and_Found/notification-center", methods=['GET', 'POST'])
def notification_center():
    return render_template('Lost_and_Found/notification-center.html')

# 智能客服路由
@app.route("/Lost_and_Found/AI-qa", methods=['GET', 'POST'])
def AI_qa():
    return render_template('Lost_and_Found/AI-qa.html')

# found动态物品详情路由
@app.route('/Lost_and_Found/founditem-detail', methods=['GET', 'POST'])
def founditem_detail():
    item_id = request.args.get('item_id', type=uuid.UUID)  # 获取查询参数
    if not item_id:
        abort(404)
    item = FoundItem.query.get_or_404(item_id)
    return render_template('Lost_and_Found/founditem-detail.html', item=item)

# 动态物品详情路由
@app.route('/Lost_and_Found/item-detail', methods=['GET', 'POST'])
def item_detail():
    item_id = request.args.get('item_id', type=uuid.UUID)  # 获取查询参数
    if not item_id:
        abort(404)
    item = LostItem.query.get_or_404(item_id)

    # 获取相似度匹配结果
    matching_results = get_matching_results(item_id)
    return render_template('Lost_and_Found/item-detail.html', item=item, matching_results=matching_results)

def get_matching_results(item_id):
    # 屎山start
    import torch
    import torchvision.transforms as transforms
    from torchvision.models import resnet50
    from PIL import Image
    import torch.nn.functional as F
    import os
    import requests
    from io import BytesIO
    import warnings
    import re
    from sklearn.decomposition import TruncatedSVD
    import numpy as np
    from sentence_transformers import SentenceTransformer, models
    # 忽略不必要的警告
    warnings.filterwarnings("ignore")
    # 模型文件名（直接放在同级目录）
    MODEL_FILE = "resnet50.pth"

    # 从URL下载图片
    def download_image_from_url(url):
        """从URL下载图片并返回PIL Image对象"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            return Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            raise RuntimeError(f"图片下载失败: {e}")

    def load_pretrained_model():
        """加载预训练模型（优先从同级目录加载）"""
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 尝试从同级目录加载模型
        if os.path.exists(MODEL_FILE):
            print("从本地加载预训练模型...")
            model = resnet50(pretrained=False)
            model.load_state_dict(torch.load(MODEL_FILE, map_location=device))
        else:
            print("从网络下载预训练模型并保存到本地...")
            model = resnet50(pretrained=True)
            torch.save(model.state_dict(), MODEL_FILE)
            print(f"模型已保存到: {os.path.abspath(MODEL_FILE)}")

        # 去掉最后的分类层
        model = torch.nn.Sequential(*list(model.children())[:-1])
        model.eval().to(device)
        return model, device

    # 加载模型（仅加载一次）
    model, device = load_pretrained_model()

    # 图像预处理
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # ImageNet 预训练模型的均值
            std=[0.229, 0.224, 0.225]
        )
    ])

    def extract_features_from_image(image):
        """从PIL Image对象提取图像的特征向量（ResNet50）"""
        try:
            image = transform(image).unsqueeze(0).to(device)
            with torch.no_grad():
                features = model(image).squeeze()
                features = features / features.norm()  # L2归一化
            return features
        except Exception as e:
            raise RuntimeError(f"特征提取失败: {e}")

    # 通过物品ID计算相似度
    def load_image(image_url):
        """根据图片URL加载图片，支持本地路径和http(s)链接"""
        if image_url.startswith('/uploads/'):
            # 假设uploads文件夹在项目根目录
            local_path = os.path.join(os.path.dirname(__file__), image_url.lstrip('/'))
            if not os.path.exists(local_path):
                raise FileNotFoundError(f"本地图片不存在: {local_path}")
            return Image.open(local_path).convert("RGB")
        elif image_url.startswith('http://') or image_url.startswith('https://'):
            return download_image_from_url(image_url)
        else:
            raise ValueError(f"不支持的图片路径: {image_url}")

    def calculate_image_similarity_by_ids(lost_item_id1, found_item_id1):
        """
        通过两个物品ID计算图片相似度
        """
        lost_item = LostItem.query.get(lost_item_id1)
        found_item = FoundItem.query.get(found_item_id1)

        # 获取两张图片的URL
        url1 = lost_item.image_url
        url2 = found_item.image_url

        # 加载图片
        image1 = load_image(url1)
        image2 = load_image(url2)

        # 提取特征
        feat1 = extract_features_from_image(image1)
        feat2 = extract_features_from_image(image2)

        # 计算相似度
        similarity_1 = F.cosine_similarity(feat1, feat2, dim=0).item()
        similarity = round(similarity_1, 4)  # 相似度

        return similarity

    def calculate_text_similarity_by_ids(lost_item_id, found_item_id):
        model_name = "./text2vec-base-chinese"
        word_embedding_model = models.Transformer(model_name)
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                       pooling_mode_mean_tokens=True)
        model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
        stopwords = set(['的', '了', '和', '是', '就', '都', '而', '及', '与', '在', '这', '那', '有', '无', '我',
                         '他', '她', '它', '我们', '你们', '他们',
                         '这', '那', '这些', '那些', '啊', '呀', '吧', '呢', '吗', '啦', '色', ' ', '\t', '\n', '“',
                         '”', '‘', '’', '（', '）', '【', '】',
                         '—', '-', '_', '=', '+', '*', '/', '\\', '|', '~', '`', '!', '@', '#', '$', '%', '^', '&',
                         '(', ')', '{', '}', '[', ']', ';',
                         ':', '"', "'", '<', '>', ',', '《', '》', '.', '?', '。', '，', '、', '；', '：', '？', '！', '“',
                         '”', '‘', '’', '（', '）', '【', '】', '…'])
        lost_item = LostItem.query.get(lost_item_id)
        found_item = FoundItem.query.get(found_item_id)
        lost_description = lost_item.description
        found_description = found_item.description

        lost_tokens = re.findall(r'\w+', lost_description)
        found_tokens = re.findall(r'\w+', found_description)

        lost_text = " ".join([t for t in lost_tokens if t not in stopwords])
        found_text = " ".join([t for t in found_tokens if t not in stopwords])

        lost_vector = model.encode([lost_text])[0]
        found_vector = model.encode([found_text])[0]

        # 归一化向量（降维前需确保向量已归一化）
        lost_vector = lost_vector / np.linalg.norm(lost_vector)
        found_vector = found_vector / np.linalg.norm(found_vector)

        # 用两个向量拟合SVD（单个向量无法拟合，需合并为矩阵）
        svd = TruncatedSVD(n_components=50)
        combined_vectors = np.vstack([lost_vector, found_vector])
        svd.fit(combined_vectors)

        # 对两个向量分别降维
        lost_vector = svd.transform([lost_vector])[0]
        found_vector = svd.transform([found_vector])[0]

        similarity = np.dot(lost_vector, found_vector) / (np.linalg.norm(lost_vector) * np.linalg.norm(found_vector))
        return similarity

    # 陈宇昂-更新-20250720
    uuids_list = []
    similarity_list = []
    text_similarity_list = []
    image_similarity_list = []

    lost_item = LostItem.query.get(item_id)
    # 获取所有拾物记录
    found_items = FoundItem.query.all()

    for found_item in found_items:
        uuids_list.append(found_item.id)
        # 调用 text_match 函数计算相似度
        text_similarity = calculate_text_similarity_by_ids(lost_item.id, found_item.id)
        text_similarity_list.append(float(text_similarity))  # 转换为Python float
        # 调用 image_match 函数计算相似度
        image_similarity = calculate_image_similarity_by_ids(lost_item.id, found_item.id)
        image_similarity_list.append(float(image_similarity))  # 转换为Python float
        # 计算加权值
        similarity = 0.3 * text_similarity + 0.7 * image_similarity
        similarity_list.append(float(similarity))  # 转换为Python float

    # 按浮点数排序
    combined = list(zip(uuids_list, similarity_list, text_similarity_list, image_similarity_list))
    sorted_data = sorted(combined, key=lambda x: x[1], reverse=True)

    matching_results = []
    for uuid_val, float_val, float_val1, float_val2 in sorted_data:
        found_item = FoundItem.query.get(uuid_val)
        result = {
            'id': uuid_val,
            'image_url': found_item.image_url,
            'name': found_item.name,
            'description': found_item.description,
            'found_date': found_item.found_date,
            'found_location': found_item.found_location,
            'text_similarity': float_val1,
            'image_similarity': float_val2,
            'similarity': float_val
        }
        matching_results.append(result)

    return matching_results


# 静态物品详情路由（示例）
@app.route("/Lost_and_Found/static-item-detail", methods=['GET', 'POST'])
def static_item_detail():
    return render_template('Lost_and_Found/static-item-detail.html')

# 登录界面路由
@app.route("/Lost_and_Found/Lost-and-Found-login", methods=['GET', 'POST'])
def Lost_and_Found_login():
    return render_template('Lost_and_Found/Lost-and-Found-login.html')

# 登录后界面路由
@app.route("/Lost_and_Found/Lost-and-Found-index-loged", methods=['GET', 'POST'])
def Lost_and_Found_index_loged():
    return render_template('Lost_and_Found/Lost-and-Found-index-loged.html')

# 用户资料路由
@app.route("/Lost_and_Found/User-Information", methods=['GET', 'POST'])
def User_Information():
    return render_template('Lost_and_Found/User-Information.html')

# 失物列表路由
@app.route("/Lost_and_Found/lost-latest", methods=['GET', 'POST'])
def lost_latest():
    return render_template('Lost_and_Found/lost-latest.html')

# 拾物列表路由
@app.route("/Lost_and_Found/found-latest", methods=['GET', 'POST'])
def found_latest():
    return render_template('Lost_and_Found/found-latest.html')

# 智能匹配路由
@app.route("/Lost_and_Found/item-search", methods=['GET', 'POST'])
def item_search():
    return render_template('Lost_and_Found/item-search.html')

# 管理员审查界面路由
@app.route("/Lost_and_Found/admin-review", methods=['GET', 'POST'])
def admin_review():
    return render_template('Lost_and_Found/admin-review.html')

# 管理员分析界面路由
@app.route("/Lost_and_Found/admin-analysis", methods=['GET', 'POST'])
def admin_analysis():
    return render_template('Lost_and_Found/admin-analysis.html')

# -------------------------- 1. 失物发布相关接口 --------------------------
# 对应架构设计中“失物发布相关接口”的接口1：创建失物信息接口
# 刘锦坤-后端1-更新-20250717
@app.route('/api/lost', methods=['POST'])
def create_lost_item():
    """创建失物信息接口
    输入：用户表单数据（JSON格式）
    输出：创建成功的物品ID
    """
    data = request.json  # 获取前端提交的表单数据
    item_id = generate_uuid()  # 生成唯一物品ID

    # 创建新的失物记录
    new_item = LostItem(
        id=item_id,
        user_id=data['user_id'],  # 用户ID
        item_type=data['item_type'],  # 物品类型
        name=data['item_name'],  # 物品名称
        description=data['item_description'],  # 物品描述
        lost_date=datetime.datetime.strptime(data['lost_date'], '%Y-%m-%d').date(),  # 丢失日期
        lost_location=data['lost_location'],  # 丢失地点
        contact_name=data['contact_name'],  # 联系人
        contact_phone=data['contact_phone'],  # 联系电话
        image_url =data['image_url'] # 图片url
    )

    db.session.add(new_item)  # 添加到数据库会话
    db.session.commit()  # 提交保存
    return jsonify({'item_id': item_id}), 201  # 返回物品ID


# 对应架构设计中“寻物发布相关接口”的接口2：上传寻物图片接口
# 付天乐-后端2-更新-20250717
@app.route('/api/lost/image/ai', methods=['POST'])
def upload_lost_image():
    """上传寻物（拾物）图片接口
    输入：图片文件
    输出：图片URL及AI识别结果（调用语义匹配接口处理）
    """
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'error': '缺少文件'}), 400

    file = request.files['file']  # 获取上传的图片文件

    # 检查是否选择了文件
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if file:
        # 生成唯一文件名（避免重复）
        import uuid
        filename = f"{str(uuid.uuid4())}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 拼接文件路径
        file.save(filepath)  # 保存文件
        image_url = f"/uploads/{filename}"  # 生成图片访问URL

        try:
            # 调用recognition.py中的图片识别函数
            description = call_qianfan_api(API_KEY_2, MODEL_ID_2, filepath, PROMPT_2)
            ai_result = {
                'features': [description],  # 物品特征描述
                'confidence': 100  # 假设置信度为100%，可根据实际情况调整
            }
        except Exception as e:
            ai_result = {
                'features': [f'识别出错: {str(e)}'],
                'confidence': 0
            }

        return jsonify({
            'image_url': image_url,  # 图片访问URL
            'ai_recognition_result': ai_result  # AI识别结果
        }), 200

    return jsonify({'error': '文件上传失败'}), 500


# 对应架构设计中“失物发布相关接口”的接口4：删除失物信息接口
@app.route('/api/lost/<item_id>', methods=['DELETE'])
def delete_lost_item(item_id):
    """删除失物信息接口
    输入：物品ID
    输出：操作状态
    """
    # 查询要删除的失物
    item = LostItem.query.get(item_id)
    if not item:
        return jsonify({'error': '物品不存在'}), 404

    db.session.delete(item)  # 从数据库删除
    db.session.commit()  # 提交修改
    return jsonify({'status': 'success'}), 200


# -------------------------- 2. 寻物发布相关接口 --------------------------
# 对应架构设计中“寻物发布相关接口”的接口1：创建寻物信息接口
# 刘锦坤-后端1-更新-20250717
@app.route('/api/found', methods=['POST'])
def create_found_item():
    """创建寻物（拾物）信息接口
    输入：用户表单数据（JSON格式）
    输出：创建成功的物品ID
    """
    data = request.json  # 获取前端提交的表单数据
    item_id = generate_uuid()  # 生成唯一物品ID

    # 刘锦坤-更新-20250719
    # 创建新的拾物记录
    new_item = FoundItem(
        id=item_id,
        user_id=data['user_id'],  # 用户ID
        item_type=data['item_type'],  # 物品类型
        name=data['item_name'],  # 物品名称
        description=data['item_description'],  # 物品描述
        found_date=datetime.datetime.strptime(data['found_date'], '%Y-%m-%d').date(),  # 拾获日期
        found_location=data['found_location'],  # 拾获地点
        storage_option=data['storage_option'],  # 存放方式
        contact_name=data['contact_name'],  # 联系人
        contact_phone=data['contact_phone'],  # 联系电话
        image_url=data['image_url']  # 图像url
    )

    db.session.add(new_item)  # 添加到数据库会话
    db.session.commit()  # 提交保存
    return jsonify({'item_id': item_id}), 201  # 返回物品ID


# 对应架构设计中“寻物发布相关接口”的接口2：上传寻物图片接口
# 付天乐-后端2-更新-20250717
# 原先为image/AI，目前已改正为image/ai，陈宇昂-20250718
@app.route('/api/found/image/ai', methods=['POST'])
# 对应架构设计中“寻物发布相关接口”的接口2：上传寻物图片接口
def upload_found_image():
    """上传寻物（拾物）图片接口
    输入：图片文件
    输出：图片URL及AI识别结果（调用语义匹配接口处理）
    """
    # 检查请求中是否包含文件
    if 'file' not in request.files:
        return jsonify({'error': '缺少文件'}), 400

    file = request.files['file']  # 获取上传的图片文件

    # 检查是否选择了文件
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if file:
        # 生成唯一文件名（避免重复）
        import uuid
        filename = f"{str(uuid.uuid4())}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 拼接文件路径
        file.save(filepath)  # 保存文件
        image_url = f"/uploads/{filename}"  # 生成图片访问URL

        try:
            # 调用recognition.py中的图片识别函数
            description = call_qianfan_api(API_KEY_2, MODEL_ID_2, filepath, PROMPT_2)
            ai_result = {
                'features': [description],  # 物品特征描述
                'confidence': 100  # 假设置信度为100%，可根据实际情况调整
            }
        except Exception as e:
            ai_result = {
                'features': [f'识别出错: {str(e)}'],
                'confidence': 0
            }

        return jsonify({
            'image_url': image_url,  # 图片访问URL
            'ai_recognition_result': ai_result  # AI识别结果
        }), 200

    return jsonify({'error': '文件上传失败'}), 500

# -------------------------- 3. 信息展示相关接口 --------------------------
# 新增接口：获取最近丢失物品信息
# 陈宇昂-更新-20250718
@app.route('/api/lost/latest/index', methods=['GET'])
def index_get_latest_lost_items():
    latest_lost_items = LostItem.query.order_by(LostItem.created_at.desc()).limit(5).all()
    lost_items_list = []
    for item in latest_lost_items:
        lost_items_list.append({
            'id': item.id,
            'item_type': item.item_type,
            'name': item.name,
            'description': item.description,
            'lost_date': item.lost_date.strftime('%Y-%m-%d'),
            'lost_location': item.lost_location,
            'contact_name': item.contact_name,
            'contact_phone': item.contact_phone,
            'image_url': item.image_url,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': item.status
        })
    return jsonify(lost_items_list)

# 新增接口：获取最近拾到物品信息
# 陈宇昂-更新-20250718
@app.route('/api/found/latest/index', methods=['GET'])
def index_get_latest_found_items():
    latest_found_items = FoundItem.query.order_by(FoundItem.created_at.desc()).limit(5).all()
    found_items_list = []
    for item in latest_found_items:
        found_items_list.append({
            'id': item.id,
            'item_type': item.item_type,
            'name': item.name,
            'description': item.description,
            'found_date': item.found_date.strftime('%Y-%m-%d'),
            'found_location': item.found_location,
            'storage_option': item.storage_option,
            'contact_name': item.contact_name,
            'contact_phone': item.contact_phone,
            'image_url': item.image_url,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': item.status
        })
    return jsonify(found_items_list)

# 对应架构设计中“信息展示相关接口”的接口1：获取最新失物列表接口
@app.route('/api/lost/latest', methods=['GET'])
def get_latest_lost_items():
    """获取最新失物列表接口
    输入：分页参数（page, per_page）
    输出：失物卡片数据数组
    """
    # 获取分页参数，默认第1页，每页10条
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # 分页查询最新失物（按创建时间倒序）
    pagination = LostItem.query.order_by(LostItem.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # 格式化返回结果
    items = [{
        'id': item.id,
        'name': item.name,
        'type': item.item_type,
        'lost_date': item.lost_date.strftime('%Y-%m-%d'),
        'lost_location': item.lost_location,
        'image_url': item.image_url,
        'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
    } for item in pagination.items]

    return jsonify({
        'items': items,  # 失物列表数据
        'total': pagination.total,  # 总条数
        'pages': pagination.pages,  # 总页数
        'page': page  # 当前页码
    }), 200


# 对应架构设计中“信息展示相关接口”的接口2：获取最新寻物列表接口
@app.route('/api/found/latest', methods=['GET'])
def get_latest_found_items():
    """获取最新寻物列表接口
    输入：分页参数（page, per_page）
    输出：寻物卡片数据数组
    """
    # 获取分页参数，默认第1页，每页10条
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # 分页查询最新拾物（按创建时间倒序）
    pagination = FoundItem.query.order_by(FoundItem.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # 格式化返回结果
    items = [{
        'id': item.id,
        'name': item.name,
        'type': item.item_type,
        'found_date': item.found_date.strftime('%Y-%m-%d'),
        'found_location': item.found_location,
        'image_url': item.image_url,
        'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
    } for item in pagination.items]

    return jsonify({
        'items': items,  # 拾物列表数据
        'total': pagination.total,  # 总条数
        'pages': pagination.pages,  # 总页数
        'page': page  # 当前页码
    }), 200

# -------------------------- 7. AI客服接口 --------------------------
# 对应架构设计中“预测服务接口”的接口：智能客服问答接口
# 刘宇扬-更新-20250717
@app.route('/api/chatbot/query', methods=['POST'])
def chatbot_query():
    """智能客服问答接口
    输入：用户问题文本
    输出：回答文本
    """
    chat_instance = QianfanChat(API_KEY_5)
    data = request.json
    if 'question' not in data:
        return jsonify({'error': '缺少问题文本'}), 400

    question = data['question']
    answer = chat_instance.call_model(question)

    return jsonify({'answer': answer}), 200

# -------------------------- 静态文件访问 --------------------------
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """提供上传图片的访问路径"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 应用入口
if __name__ == '__main__':
    app.run(debug=True)  # 启动应用，开启调试模式