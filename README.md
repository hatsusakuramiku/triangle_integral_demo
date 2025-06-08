# 三角形积分演示项目

这是一个用于演示三角形区域上数值积分的 Web 应用程序。该项目提供了一个直观的界面来可视化不同的三角形积分公式，并计算给定函数在三角形区域上的积分值。

## 功能特点

- 支持多种三角形积分公式的可视化展示
- 实时计算三角形区域上的函数积分
- 交互式三角形绘制和节点显示
- 支持 LaTeX 格式的数学表达式输入
- 自动计算三角形面积
- 在线和离线模式支持

## 安装说明

1. 克隆仓库：

   ```bash
   git clone https://github.com/yourusername/triangle_integral_demo.git
   cd triangle_integral_demo
   ```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动应用：

   ```bash
   python src/main.py
   ```

2. 在浏览器中访问 `http://localhost:5000`

3. 使用界面：
   - 选择或输入三角形顶点坐标
   - 选择积分公式
   - 输入要积分的函数（支持 LaTeX 格式）
   - 点击计算按钮获取结果

## 部署

该项目支持部署到 Vercel 平台。配置文件`vercel.json`已经包含必要的部署设置。

### Vercel 部署步骤

1. 安装 Vercel CLI（如果尚未安装）：

    ```bash
    npm install -g vercel
    ```

2. 登录 Vercel 账号：

    ```bash
    vercel login
    ```

3. 在项目根目录下运行部署命令：

    ```bash
    vercel
    ```

4. 按照提示完成部署：

   - 选择项目范围（个人或团队）
   - 确认项目名称
   - 确认项目根目录
   - 确认部署设置

5. 部署完成后，Vercel 会提供一个项目访问链接

### 环境变量配置

如果需要配置环境变量，可以在 Vercel 项目设置中的 "Environment Variables" 部分添加：

- `PYTHON_VERSION`: 3.11
- 其他必要的环境变量

### 自动部署

- 当您推送代码到 GitHub 仓库时，Vercel 会自动触发新的部署
- 可以在 Vercel 仪表板中查看部署历史和状态
- 支持预览部署（Preview Deployments）用于测试更改

### 注意事项

- 确保 `requirements.txt` 文件包含所有必要的依赖
- 检查 `vercel.json` 配置是否正确
- 确保所有静态文件都放在 `src/static` 目录下

## 项目结构

```fileTree
triangle_integral_demo/
├── src/
│   ├── main.py              # 主应用程序
│   ├── static/              # 静态文件
│   ├── models/              # 数据模型
│   ├── routes/              # 路由定义
│   └── triangle_formula.json # 积分公式数据
├── requirements.txt         # 项目依赖
└── vercel.json             # Vercel部署配置
```

## 许可证

MIT License
