### 项目结构

```shell
├── ./templates
│   ├── index.html # 达内官网相关文件
│   ├── base.html
│   ├── ...
│   └── ./Lost_and_Found # 第九组所有文件
│       ├── Lost-and-Found-index.html
│       ├── lost-post.html
│       ├── item-detail.html
│       ├── found-post.html
│       ├── ... # 外层存放前端诸文件
│       └── ./backend # backend文件夹中存放后端诸文件 
│           ├── chatbot.py # 后端5-智能客服程序
│           └── recognition.py # 后端2-图像识别程序
│
├── ./static # 存放达内官网诸CSS和JS文件
├── ./uploads # 存放上传的文件
├── ./text2vec-base-chinese # 文本匹配模块的预训练模型
│   ├── config.json
│   ├── model.safetensors 
│   ├── modules.json
│   ├── sentence_bert_config.json
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── vocab.txt
│
├── resnet50.pth # 图像匹配模块调用的模型
└── app.py # 主程序入口
```