<div align="center">

# 🚀 JSONVoyager

**Interactive Terminal JSON Explorer & Processor**

*轻量级终端JSON交互式浏览与处理引擎*

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey)](.)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)](.)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

## 简体中文

### 🎉 项目介绍

JSONVoyager 是一款**零依赖**的轻量级终端JSON交互式浏览与处理工具。它解决了开发者在终端中处理JSON数据时缺乏可视化、交互式体验的痛点。

**灵感来源**：jq 虽强大但学习曲线陡峭，且缺乏交互式体验。JSONVoyager 提供直观的树形浏览、扁平化视图、表格视图，以及搜索、过滤、导出等功能，让JSON数据处理变得轻松愉快。

**自研差异化亮点**：
- 🎯 **零依赖**：纯Python标准库实现，无需安装任何第三方包
- 🌈 **彩色输出**：内置ANSI颜色系统，自动识别终端类型
- 📊 **多视图模式**：树形、扁平、表格三种视图自由切换
- 🔍 **实时搜索**：支持关键词高亮和路径搜索
- 📤 **多格式导出**：JSON、JSONL、CSV、YAML一键导出

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🌳 **树形视图** | 层级化展示JSON结构，支持折叠/展开 |
| 📋 **扁平视图** | 一键展开所有键值对，路径一目了然 |
| 📊 **表格视图** | 对象数组以表格形式展示，清晰直观 |
| 🔍 **智能搜索** | 支持键名和值内容搜索，结果高亮显示 |
| 📤 **格式导出** | 支持 JSON/JSONL/CSV/YAML 导出 |
| 📈 **数据统计** | 实时统计键值、数组、字符串等数量 |
| 🎯 **路径查询** | 支持点符号路径查询（如 `users.0.name`） |
| 🎨 **彩色终端** | 自动类型着色，提升可读性 |

### 🚀 快速开始

#### 环境要求
- Python 3.7+
- 终端支持ANSI颜色（可选）

#### 安装

```bash
# 方式一：直接下载使用
wget https://raw.githubusercontent.com/gitstq/JSONVoyager/main/jsonvoyager.py
python3 jsonvoyager.py your-data.json

# 方式二：通过 pip 安装
pip install jsonvoyager
jsonvoyager your-data.json
```

#### 基本用法

```bash
# 交互式浏览JSON文件
jsonvoyager data.json

# 从URL加载JSON
jsonvoyager https://api.example.com/data.json

# 从stdin读取
cat data.json | jsonvoyager -

# 查询特定路径
jsonvoyager data.json -q "users.0.name"

# 查看统计信息
jsonvoyager data.json --stats

# 扁平化展示
jsonvoyager data.json --flatten

# 彩色输出
jsonvoyager data.json --colorize

# 导出为CSV
jsonvoyager data.json --export csv -o output.csv
```

#### 交互模式命令

| 命令 | 说明 |
|------|------|
| `h` | 显示帮助 |
| `q` | 退出 |
| `tree` | 切换树形视图 |
| `flat` | 切换扁平视图 |
| `table` | 切换表格视图 |
| `q <path>` | 查询路径 |
| `s <keyword>` | 搜索关键词 |
| `stats` | 显示统计 |
| `export <format>` | 导出数据 |
| `c` | 彩色JSON输出 |
| `r` | 重新加载文件 |

### 📖 详细使用指南

#### 树形视图
```
└── [+] 📁 project: "JSONVoyager"
    ├──   "#" version: "1.0.0"
    ├── [+] 📁 author: object (3 keys)
    │   ├──   "\" name: "gitstq"
    │   └──   "\" github: "https://github.com/gitstq"
    └── [+] 📊 features: array [7]
        ├──   [0] "\" Interactive TUI
        └──   [1] "\" Tree View
```

#### 路径查询示例
```bash
$ jsonvoyager sample.json -q "users.0.name"
"Alice Chen"

$ jsonvoyager sample.json -q "stats.license"
"MIT"
```

#### 导出示例
```bash
# 导出为CSV（适用于对象数组）
jsonvoyager data.json --export csv -o output.csv

# 导出为YAML
jsonvoyager data.json --export yaml -o output.yaml

# 导出为JSONL
jsonvoyager data.json --export jsonl -o output.jsonl
```

### 💡 设计思路与迭代规划

**技术选型原因**：
- 纯Python标准库：确保零依赖，跨平台兼容
- ANSI颜色：广泛支持的终端着色方案
- 模块化设计：易于扩展新视图和导出格式

**后续迭代计划**：
- [ ] JSON Schema验证
- [ ] 数据对比（diff）功能
- [ ] 正则表达式搜索
- [ ] 批量文件处理
- [ ] 插件系统

### 📦 打包与部署

```bash
# 本地安装
pip install -e .

# 构建分发包
make build

# 运行测试
make test
```

### 🤝 贡献指南

欢迎提交Issue和PR！请遵循以下规范：
- 提交前运行测试：`python test_jsonvoyager.py`
- 代码风格：PEP 8
- 提交信息格式：`feat:`, `fix:`, `docs:`, `refactor:`

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

JSONVoyager 是一款**零依賴**的輕量級終端JSON交互式瀏覽與處理工具。它解決了開發者在終端中處理JSON資料時缺乏視覺化、交互式體驗的痛點。

**自研差異化亮點**：
- 🎯 **零依賴**：純Python標準庫實現
- 🌈 **彩色輸出**：內建ANSI顏色系統
- 📊 **多視圖模式**：樹形、扁平、表格三種視圖
- 🔍 **即時搜尋**：支援關鍵詞高亮和路徑搜尋
- 📤 **多格式匯出**：JSON、JSONL、CSV、YAML

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🌳 **樹形視圖** | 層級化展示JSON結構，支援摺疊/展開 |
| 📋 **扁平視圖** | 一鍵展開所有鍵值對 |
| 📊 **表格視圖** | 物件陣列以表格形式展示 |
| 🔍 **智慧搜尋** | 支援鍵名和值內容搜尋 |
| 📤 **格式匯出** | 支援 JSON/JSONL/CSV/YAML |
| 📈 **資料統計** | 即時統計鍵值、陣列等數量 |
| 🎯 **路徑查詢** | 支援點符號路徑查詢 |
| 🎨 **彩色終端** | 自動類型著色 |

### 🚀 快速開始

```bash
# 安裝
pip install jsonvoyager

# 交互式瀏覽
jsonvoyager data.json

# 查詢路徑
jsonvoyager data.json -q "users.0.name"

# 匯出CSV
jsonvoyager data.json --export csv -o output.csv
```

### 📄 開源協議

[MIT License](LICENSE)

---

## English

### 🎉 Introduction

JSONVoyager is a **zero-dependency** lightweight terminal JSON interactive explorer and processor. It solves the pain point of developers lacking visual, interactive experiences when processing JSON data in the terminal.

**Differentiation Highlights**:
- 🎯 **Zero Dependencies**: Pure Python standard library
- 🌈 **Colorized Output**: Built-in ANSI color system
- 📊 **Multi-View Modes**: Tree, flat, and table views
- 🔍 **Real-time Search**: Keyword highlighting and path search
- 📤 **Multi-format Export**: JSON, JSONL, CSV, YAML

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🌳 **Tree View** | Hierarchical JSON display with fold/unfold |
| 📋 **Flat View** | One-click flatten all key-value pairs |
| 📊 **Table View** | Object arrays in table format |
| 🔍 **Smart Search** | Search by key name and value content |
| 📤 **Format Export** | JSON/JSONL/CSV/YAML support |
| 📈 **Data Stats** | Real-time statistics |
| 🎯 **Path Query** | Dot notation path queries |
| 🎨 **Color Terminal** | Auto type coloring |

### 🚀 Quick Start

```bash
# Install
pip install jsonvoyager

# Interactive explore
jsonvoyager data.json

# Query path
jsonvoyager data.json -q "users.0.name"

# Export to CSV
jsonvoyager data.json --export csv -o output.csv
```

### 📄 License

[MIT License](LICENSE)

---

<div align="center">

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
