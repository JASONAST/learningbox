# 学习工具箱 (Learning Toolbox)

一个基于 Python 的桌面任务管理应用程序，使用 tkintertools (由 Xiaokang2022 设计) 并集成了任务管理功能。

## 功能特性

### 任务管理
- 创建、编辑和删除任务
- 设置任务截止日期和重要程度
- 分配优先级（颜色编码）
- 添加任务描述
- 番茄工作法计时器
- 多种任务排序方式

### 界面设计
- 主窗口任务卡片展示
- 迷你窗口模式
- 任务详情视图
- 设置界面
- 日期/时间选择器

### 个性化设置
- 深色/浅色主题
- 背景图片支持
- 透明度选项
- 任务颜色编码
- 排序偏好设置

### 生产力工具
- 番茄工作计时器
- 任务组织
- 视觉优先级指示

## 安装说明

### 环境要求
- Python 3.12+
- pip (Python 包管理器)

### 安装步骤

1. 克隆仓库：
````bash
git clone <仓库地址>
cd learningbox-main
````

2. 安装依赖：
````bash
pip install -r requirements.txt
````

3. 安装测试依赖（可选）：
````bash
pip install -r test_requirements.txt
````

## 使用方法

### 运行应用

````bash
python main.py
````

### 开发指南

1. 初始化项目（创建默认配置文件）：
````bash
python init_project.py
````

2. 运行测试：
````bash
python -m pytest test.py -v
````

3. 构建可执行文件：
````bash
python build.py
````

### 必需文件

项目目录中必须包含以下文件：

- `main.py` - 主程序代码
- `config.json` - 应用程序配置
- `theme.json` - 主题定义
- `tasks.json` - 任务数据存储
- `task.ico` - 应用程序图标（可选）

## 构建说明

项目可以使用 PyInstaller 构建成独立的 Windows 可执行文件：

1. 运行构建脚本：
````bash
python build.py
````

2. 可执行文件将在 `dist` 目录中生成
3. 可以使用生成的 `setup.iss` 脚本创建可选的安装程序

## 项目结构

```
learningbox-main/
├── main.py              # 主程序代码
├── init_project.py      # 项目初始化脚本
├── build.py            # 构建自动化脚本
├── test.py             # 单元测试
├── config.json         # 应用程序配置
├── theme.json         # 主题定义
├── tasks.json         # 任务数据存储
├── requirements.txt    # Python 依赖
└── test_requirements.txt # 测试依赖
```

## 配置说明

应用程序使用多个 JSON 文件进行配置：

- `config.json`：常规设置（主题、排序、透明度）
- `theme.json`：UI 主题定义（颜色、样式）
- `tasks.json`：任务数据存储

## 测试

运行测试套件：
````bash
python -m pytest test.py -v
````

## 开源许可

MIT License

## 致谢

- tkintertools 库由 Xiaokang2022 开发
- 使用 Python 和 Tkinter 构建

## 贡献指南

1. Fork 仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 问题反馈

如果您在使用过程中遇到任何问题，欢迎通过以下方式反馈：
1. 在 GitHub Issues 中提出问题
2. 发送邮件至开发者邮箱
3. 在项目讨论区参与讨论
