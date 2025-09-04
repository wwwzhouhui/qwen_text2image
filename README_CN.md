中文 ｜ [English](./README.md)

[项目源码地址](https://github.com/wwwzhouhui/qwen_text2image)：

# Qwen Text2Image Dify 插件

## 📖 项目简介

这是一个基于 ModelScope Qwen-Image 模型的文生图 Dify 插件，能够根据文本描述生成高质量的图像。插件采用异步任务处理模式，确保稳定可靠的图像生成体验。

## ✨ 功能特点

- 🎨 **高质量图像生成**：基于 Qwen-Image 先进的 AI 模型
- ⚡ **异步处理**：采用任务提交+轮询的异步模式，避免超时
- 🔄 **实时反馈**：提供详细的生成进度和状态信息
- 🛡️ **错误处理**：完善的异常处理和用户友好的错误提示
- 🌐 **中英双语**：支持中英文界面和提示信息

## 🏗️ 项目架构

```
qwen_text2image_plugin/
├── manifest.yaml              # 插件清单文件
├── main.py                   # 插件入口文件
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量示例
├── README.md                # 项目文档
├── icon.svg                 # 插件图标
├── provider/                # 服务提供者配置
│   ├── __init__.py
│   ├── modelscope.yaml      # ModelScope 提供者配置
│   └── modelscope_provider.py
└── tools/                   # 工具实现
    ├── __init__.py
    ├── text2image.yaml      # 文生图工具配置
    └── text2image.py        # 文生图工具实现
```

## 🚀 快速开始

### 1. 获取 ModelScope API Key

1. 访问 [ModelScope 官网](https://modelscope.cn)
2. 注册并登录账户
3. 前往 [我的访问令牌](https://modelscope.cn/my/myaccesstoken) 页面
4. 创建新的 API Key（格式为 `ms-xxxxxx`）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

复制 `.env.example` 为 `.env` 并配置相关参数：

```bash
cp .env.example .env
```

### 4. 在 Dify 中安装插件

1. 将插件文件夹上传到 Dify 插件目录
2. 在 Dify 管理界面中启用插件
3. 配置 ModelScope API Key

## 🔧 使用方法

### 基本用法

1. 在 Dify 工作流中添加 "Qwen 文生图" 工具

2. 配置 ModelScope API Key

      ![image-20250820103320281](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250820103320281.png)

   ![image-20250820103334715](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250820103334715.png)

3. 输入图像描述提示词

4. 选择模型（默认 Qwen-Image）

5. 运行工具生成图像

   工作流dsl

   ```yml
   app:
     description: ''
     icon: 🤖
     icon_background: '#FFEAD5'
     mode: advanced-chat
     name: 自定义文生图插件验证测试-chatflow
     use_icon_as_answer_icon: false
   dependencies:
   - current_identifier: null
     type: package
     value:
       plugin_unique_identifier: wwwzhouhui/qwen_text2image:0.0.1@18eb2a22be7173a6bd806402b1748b3d7e9967acd87e1b4c5a6b794fa08fca0c
   kind: app
   version: 0.3.0
   workflow:
     conversation_variables: []
     environment_variables: []
     features:
       file_upload:
         allowed_file_extensions:
         - .JPG
         - .JPEG
         - .PNG
         - .GIF
         - .WEBP
         - .SVG
         allowed_file_types:
         - image
         allowed_file_upload_methods:
         - local_file
         - remote_url
         enabled: false
         fileUploadConfig:
           audio_file_size_limit: 500
           batch_count_limit: 10
           file_size_limit: 100
           image_file_size_limit: 100
           video_file_size_limit: 500
           workflow_file_upload_limit: 10
         image:
           enabled: false
           number_limits: 3
           transfer_methods:
           - local_file
           - remote_url
         number_limits: 3
       opening_statement: ''
       retriever_resource:
         enabled: true
       sensitive_word_avoidance:
         enabled: false
       speech_to_text:
         enabled: false
       suggested_questions: []
       suggested_questions_after_answer:
         enabled: false
       text_to_speech:
         enabled: false
         language: ''
         voice: ''
     graph:
       edges:
       - data:
           isInIteration: false
           isInLoop: false
           sourceType: start
           targetType: tool
         id: 1755656337314-source-1755657278812-target
         source: '1755656337314'
         sourceHandle: source
         target: '1755657278812'
         targetHandle: target
         type: custom
         zIndex: 0
       - data:
           isInLoop: false
           sourceType: tool
           targetType: answer
         id: 1755657278812-source-answer-target
         source: '1755657278812'
         sourceHandle: source
         target: answer
         targetHandle: target
         type: custom
         zIndex: 0
       nodes:
       - data:
           desc: ''
           selected: false
           title: 开始
           type: start
           variables: []
         height: 53
         id: '1755656337314'
         position:
           x: 80
           y: 282
         positionAbsolute:
           x: 80
           y: 282
         selected: false
         sourcePosition: right
         targetPosition: left
         type: custom
         width: 244
       - data:
           answer: '{{#1755657278812.text#}}
   
             {{#1755657278812.files#}}
   
             '
           desc: ''
           selected: false
           title: 直接回复
           type: answer
           variables: []
         height: 123
         id: answer
         position:
           x: 740
           y: 282
         positionAbsolute:
           x: 740
           y: 282
         selected: true
         sourcePosition: right
         targetPosition: left
         type: custom
         width: 244
       - data:
           desc: ''
           is_team_authorization: true
           output_schema: null
           paramSchemas:
           - auto_generate: null
             default: null
             form: llm
             human_description:
               en_US: The text prompt to generate image from. Describe what you want
                 to see in the image in detail. For example "A golden cat sitting on
                 a red sofa in a cozy living room".
               ja_JP: The text prompt to generate image from. Describe what you want
                 to see in the image in detail. For example "A golden cat sitting on
                 a red sofa in a cozy living room".
               pt_BR: The text prompt to generate image from. Describe what you want
                 to see in the image in detail. For example "A golden cat sitting on
                 a red sofa in a cozy living room".
               zh_Hans: The text prompt to generate image from. Describe what you want
                 to see in the image in detail. For example "A golden cat sitting on
                 a red sofa in a cozy living room".
             label:
               en_US: Prompt
               ja_JP: Prompt
               pt_BR: Prompt
               zh_Hans: Prompt
             llm_description: Text prompt that describes the desired image content in
               detail. The more specific and descriptive, the better the generated image
               quality.
             max: null
             min: null
             name: prompt
             options: []
             placeholder: null
             precision: null
             required: true
             scope: null
             template: null
             type: string
           - auto_generate: null
             default: Qwen/Qwen-Image
             form: form
             human_description:
               en_US: The AI model to use for image generation. Qwen-Image is the default
                 and recommended model.
               ja_JP: The AI model to use for image generation. Qwen-Image is the default
                 and recommended model.
               pt_BR: The AI model to use for image generation. Qwen-Image is the default
                 and recommended model.
               zh_Hans: The AI model to use for image generation. Qwen-Image is the default
                 and recommended model.
             label:
               en_US: Model
               ja_JP: Model
               pt_BR: Model
               zh_Hans: Model
             llm_description: ''
             max: null
             min: null
             name: model
             options:
             - icon: ''
               label:
                 en_US: Qwen-Image (Recommended)
                 ja_JP: Qwen-Image (Recommended)
                 pt_BR: Qwen-Image (Recommended)
                 zh_Hans: Qwen-Image (Recommended)
               value: Qwen/Qwen-Image
             placeholder: null
             precision: null
             required: false
             scope: null
             template: null
             type: select
           params:
             model: ''
             prompt: ''
           provider_id: wwwzhouhui/qwen_text2image/modelscope
           provider_name: wwwzhouhui/qwen_text2image/modelscope
           provider_type: builtin
           selected: false
           title: Text to Image
           tool_configurations:
             model:
               type: constant
               value: Qwen/Qwen-Image
           tool_description: Generate high-quality images from text prompts using ModelScope
             Qwen-Image AI model. Support various image styles and detailed descriptions.
           tool_label: Text to Image
           tool_name: text2image
           tool_parameters:
             prompt:
               type: mixed
               value: '{{#sys.query#}}'
           type: tool
           version: '2'
         height: 121
         id: '1755657278812'
         position:
           x: 384
           y: 282
         positionAbsolute:
           x: 384
           y: 282
         selected: false
         sourcePosition: right
         targetPosition: left
         type: custom
         width: 244
       viewport:
         x: 34
         y: 87.5
         zoom: 1
   ```

   ![image-20250820104750679](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250820104750679.png)

### 提示词建议

为了获得最佳的图像生成效果，建议：

- **详细描述**：提供具体的场景、对象、颜色、风格等信息
- **清晰表达**：使用简洁明了的语言描述
- **风格指定**：可以指定艺术风格，如"油画风格"、"卡通风格"等

示例提示词：
```
一只金色的猫坐在舒适客厅的红色沙发上，温暖的阳光透过窗户洒进来，营造出温馨的家庭氛围
```

## ⚙️ 技术实现

### 核心流程

1. **任务提交**：向 ModelScope API 提交异步图像生成任务
2. **状态轮询**：每 5 秒查询一次任务状态，最多等待 5 分钟
3. **图像下载**：任务完成后下载生成的图像
4. **格式转换**：使用 PIL 将图像转换为 PNG 格式返回

### API 调用模式

```python
# 1. 提交任务
POST /v1/images/generations
Headers: X-ModelScope-Async-Mode: true

# 2. 查询状态
GET /v1/tasks/{task_id}
Headers: X-ModelScope-Task-Type: image_generation

# 3. 下载图像
GET {image_url}
```

## 🔍 故障排除

### 常见问题

1. **API Key 无效**
   - 检查 API Key 格式是否以 `ms-` 开头
   - 确认 API Key 是否有效且未过期

2. **生成超时**
   - 检查网络连接是否正常
   - 尝试简化提示词描述
   - 稍后重试

3. **图像下载失败**
   - 检查网络连接
   - 确认防火墙设置允许访问 ModelScope 域名

### 错误代码

- `401`: API Key 无效或未授权
- `429`: API 调用频率过高
- `500`: 服务器内部错误

## 📋 开发规范

本插件严格遵循 [CLAUDE2.md](../CLAUDE2.md) 中定义的 Dify 文生图插件开发规范：

- ✅ 异步任务处理模式
- ✅ 完整的错误处理机制
- ✅ 实时进度反馈
- ✅ 中英文双语支持
- ✅ ModelScope API 标准调用

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个插件！

## 📄 许可证

本项目采用 MIT 许可证。

## 🔗 相关链接

- [ModelScope 官网](https://modelscope.cn)
- [Qwen-Image 模型](https://modelscope.cn/models/Qwen/Qwen-Image)
- [Dify 官方文档](https://docs.dify.ai)
- [插件开发规范](../CLAUDE2.md)