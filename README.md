# AI 产品学习内化系统

将腾讯会议课程转写加工为「笔记 + 课后自测 + 面试实战」三件套的个人学习网站。

## 在线访问（只读）

https://claudiaaaaa-1.github.io/AIPM/

## 本地编辑

```bash
cd ai-learn
python3 server.py
# 打开 http://127.0.0.1:8777
```

## 数据同步（两台电脑）

```bash
# 电脑 A 改完内容后
git add .
git commit -m "更新内容"
git push

# 电脑 B 开始工作前
git pull
```

## 文件结构

```
ai-learn/
├── index.html          # 前端单页应用
├── server.py           # 本地编辑后端（GitHub Pages 上不需要）
├── content/
│   ├── index.json      # 课程索引
│   ├── topics.json     # 主题定义
│   ├── user-takes.json # 个人笔记（跨设备同步）
│   ├── courses/        # 每节课的三件套 JSON
│   └── ...
├── sources/            # 原始转写归档
└── SOP.md              # 内容加工规范
```
