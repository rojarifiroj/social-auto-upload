# 简化项目结构

## 📁 当前目录结构

```
social-auto-upload/
├── src/                    # 源代码（保持原样）
│   ├── core/              # 核心功能
│   ├── platforms/         # 各平台实现
│   ├── utils/             # 工具模块
│   └── config/            # 配置管理
├── tools/                 # 工具脚本
│   ├── cookie_manager/    # Cookie管理工具
│   ├── upload_tools/      # 上传工具
│   └── video_processing/  # 视频处理工具
├── data/                  # 数据文件
│   ├── cookies/           # Cookie存储
│   ├── logs/              # 日志文件
│   ├── records/           # 记录文件
│   ├── titles/            # 标题文件
│   └── videos/            # 视频文件
├── assets/                # 资源文件
│   └── media/             # 媒体文件
├── docs/                  # 文档
│   ├── README.MD
│   ├── QUICKSTART.md
│   ├── CHANGELOG.md
│   ├── LICENSE
│   └── examples/          # 使用示例
├── scripts/               # 项目脚本
├── requirements.txt       # 依赖文件
├── setup.py              # 安装配置
└── .gitignore            # Git忽略文件
```

## 🎯 整理效果

✅ **工具文件分类**: 按功能将工具文件分类存放
✅ **数据文件集中**: 所有运行时数据集中管理
✅ **文档整理**: 文档文件统一存放
✅ **结构清晰**: 目录结构更加清晰易懂

## 📝 使用说明

1. **Cookie管理**: `tools/cookie_manager/`
2. **上传工具**: `tools/upload_tools/`
3. **视频处理**: `tools/video_processing/`
4. **数据存储**: `data/` 目录下对应子目录
5. **文档查看**: `docs/` 目录

## 🔄 下一步

1. 更新代码中的导入路径
2. 测试工具是否正常工作
3. 根据需要进一步优化结构
