# Course JSON Schema

每节课存储为 `content/courses/<课程ID>.json`，结构如下。

```json
{
  "id": "20261030-需求评审实战",
  "title": "需求评审实战",
  "date": "2026-10-30",
  "source": "腾讯会议转写",
  "instructor": "讲师名",
  "duration": "90min",
  "summary": "一句话总结，≤40字",
  "topics": ["requirement-review"],
  "tags": ["需求评审", "AI产品", "协作"],

  "notes": {
    "frameworks": [
      {
        "name": "框架名",
        "definition": "一句话定义",
        "scenario": "适用场景",
        "steps": ["步骤1", "步骤2"],
        "myTake": "我的理解"
      }
    ],
    "keyPoints": [
      { "point": "观点", "evidence": "论据/案例", "question": "我的追问" }
    ],
    "cases": [
      { "case": "案例/金句", "note": "说明", "useFor": "可用于" }
    ],
    "questions": ["疑问1"],
    "connections": "与已有知识/项目的连接"
  },

  "exercises": [
    {
      "level": "L1",
      "q": "题干",
      "tests": "考察点",
      "framework": "答题框架（可选）",
      "answer": "参考要点（折叠展示）"
    }
  ],

  "interview": {
    "questions": [
      {
        "type": "面试题 | 工作场景题",
        "q": "题干",
        "tests": "考察点",
        "framework": "答题框架",
        "answer": "参考要点"
      }
    ]
  },

  "personal": {
    "_note": "二期字段，一期留空",
    "mistakes": [],
    "reviewQueue": [],
    "mastery": 0
  }
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | 唯一标识，`YYYYMMDD-短标题` |
| `topics` | ✅ | 挂载的主题 ID 数组，用于主题视图聚合 |
| `notes` | ✅ | 三件套之一，结构化笔记 |
| `exercises` | ✅ | 三件套之二，课后自测题 |
| `interview` | ✅ | 三件套之三，面试 & 实战题 |
| `personal` | ⬜ | 二期个人层，一期留空对象 |
