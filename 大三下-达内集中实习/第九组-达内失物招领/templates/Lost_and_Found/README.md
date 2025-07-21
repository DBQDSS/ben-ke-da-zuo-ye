## 项目更新

### 20250714
##### 项目目录说明

我在群里发的本地运行文件的目录结构说明
```shell
├── templates
│   ├── index.html # 达内官网相关文件
│   ├── base.html
│   ├── ...
│   └── Lost_and_Found # 第九组所有文件
│       ├── Lost-and-Found-index.html
│       ├── lost-post.html
│       ├── static-item-detail.html
│       ├── found-post.html
│       ├── ... # 外层存放前端诸文件
│       └── backend # backend文件夹中存放后端诸文件
│           ├── xxx1.py
│           ├── xxx2.pth
│           ├── ...
│           └── ...
└── app.py # 主程序入口
```
安装完全部所需的库，即可运行。


### 20250715
##### 项目目录说明

我在群里发的本地运行文件的目录结构说明
```shell
├── templates
│   ├── index.html # 达内官网相关文件
│   ├── base.html
│   ├── ...
│   └── Lost_and_Found # 第九组所有文件
│       ├── Lost-and-Found-index.html
│       ├── lost-post.html
│       ├── static-item-detail.html
│       ├── found-post.html
│       ├── ... # 外层存放前端诸文件
│       └── backend # backend文件夹中存放后端诸文件
│           ├── xxx1.py
│           ├── xxx2.pth
│           ├── ...
│           └── ...
└── app.py # 主程序入口
```
安装完全部所需的库，即可运行。

##### QA提交的项目文件结构说明
两位测试人员需要提交的文件目录，将结果截图放入`测试文件夹`中

胡楷：
```shell

├── 用于测试的数据集 # 存放测试数据集
│   ├── 后端2 # 记得测试各个图片格式(jpg,png,webp)
│   │   ├── 图片1.jpg
│   │   ├── 图片2.png
│   │   ├── ...
│   │   └── 图片x.webp     
│   ├── 后端3 # 记得测试各个图片格式(jpg,png,webp)
│   │   ├── 图片1.jpg
│   │   ├── ...
│   │   └── 图片x.webp
│   ├── 后端4 # 文本匹配
│   │   └── 后端4测试文本.txt # 每行都是一个测试文本
│   └── 后端5 # 图片分类    
│       └── 后端5测试文本.txt # 将你与AI的对话写入其中
└── 本地测试截图 # 用于存放测试截图
    ├── 后端2 # 各文件夹中存放各程序截图(5张)
    ├── 后端3
    ├── 后端4
    └── 后端5
```

李雅煊：
```shell

├── 用于测试的数据集 # 存放测试数据集
│   ├── 失物发布 # 记得测试各个图片格式(jpg,png,webp)
│   │   ├── 图片1.jpg
│   │   ├── 图片2.png
│   │   ├── ...
│   │   └── 图片x.webp     
│   ├── 拾物发布 # 记得测试各个图片格式(jpg,png,webp)
│   │   ├── 图片1.jpg
│   │   ├── ...
│   │   └── 图片x.webp
│   └── AI客服    
│       └── 后端5测试文本.txt # 将你与AI的对话写入其中
└── 在线测试截图 # 用于存放测试截图
    ├── 后端2 # 各文件夹中存放各程序截图(5张)
    ├── 后端3
    ├── 后端4
    └── 后端5
```



##### 有关数据库的变动
```shell
# 注意，我们对mysql表格做了一些新定义，如果该段代码无法在您的设备上运行，请按照我们的表结构修改数据库。
# 我们定义的表结构如下：
# tbl_user:
#   - id
#   - username
#   - name
#   - password
#   - gender
#   - age

# tbl_click:
#   - id
#   - course_id
#   - course_name
#   - user_id
#   - click_time

# tbl_enroll:
#   - course_id
#   - course_name
#   - user_id
#   - enroll_time

# tbl_course:
#   - id
#   - course_name

```

db目录下有我们对几个表生成的虚假数据`5db.sql`，请根据情况使用(UTF编码)。