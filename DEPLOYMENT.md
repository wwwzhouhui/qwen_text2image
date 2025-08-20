# 🚀 Qwen Text2Image 插件部署指南

## 📋 部署前准备

### 1. 环境要求

- Python 3.12+
- Dify 平台环境
- 稳定的网络连接（能访问 ModelScope API）

### 2. 获取 ModelScope API Key

1. 访问 [ModelScope 官网](https://modelscope.cn)
2. 注册并登录账户
3. 前往 [我的访问令牌](https://modelscope.cn/my/myaccesstoken)
4. 创建新的 API Key（格式：`ms-xxxxxxxxxxxxxx`）
5. 确保 API Key 有图像生成权限

## 🔧 本地测试

### 1. 安装依赖

```bash
cd qwen_text2image_plugin
pip install -r requirements.txt
```

### 2. 设置环境变量

```bash
export MODELSCOPE_API_KEY=ms-your-actual-api-key
```

### 3. 运行测试脚本

```bash
python test_plugin.py
```

预期输出：
```
🔧 Qwen Text2Image 插件测试工具
==================================================
✅ 依赖检查通过
🚀 开始测试 Qwen Text2Image 插件...
📝 使用 API Key: ms-xxxxxxx...
🎨 测试提示词: 一只可爱的橙色小猫坐在绿色的草地上，背景是蓝天白云
🤖 使用模型: Qwen/Qwen-Image
==================================================
[1] 📄 🚀 正在提交图像生成任务...
[2] 📄 ✅ 任务已创建，ID: task_xxxxx
[3] 📄 ⏳ 正在生成图像，请稍候...
...
[N] 🖼️  图像生成成功！
     📊 图像大小: 245760 字节
     📋 MIME 类型: image/png
     💾 图像已保存为: test_output.png

✅ 测试成功！插件工作正常。
```

## 📦 Dify 平台部署

### 方法一：本地开发模式

1. **配置环境文件**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置远程安装参数
   ```

2. **启动开发服务器**
   ```bash
   python main.py
   ```

3. **在 Dify 中添加插件**
   - 进入 Dify 管理界面
   - 选择"插件管理"
   - 添加本地开发插件
   - 输入开发服务器地址

### 方法二：插件包部署

1. **打包插件**
   ```bash
   # 创建插件压缩包
   tar -czf qwen_text2image_plugin.tar.gz qwen_text2image_plugin/
   ```

2. **上传到 Dify**
   - 在 Dify 管理界面选择"插件管理"
   - 点击"上传插件"
   - 选择打包的插件文件
   - 等待安装完成

3. **配置插件**
   - 在插件列表中找到"Qwen 文生图"
   - 点击"配置"
   - 输入 ModelScope API Key
   - 保存配置

## ⚙️ 配置说明

### 必需配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| ModelScope API Key | 用于调用 ModelScope API | `ms-xxxxxxxxxxxxxx` |

### 可选配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 超时时间 | 300秒 | 图像生成最大等待时间 |
| 轮询间隔 | 5秒 | 任务状态查询间隔 |
| 最大重试次数 | 60次 | 最大轮询次数 |

## 🔍 验证部署

### 1. 插件状态检查

在 Dify 插件管理界面确认：
- ✅ 插件状态为"已启用"
- ✅ API Key 配置正确
- ✅ 没有错误提示

### 2. 功能测试

1. **创建测试工作流**
   - 新建一个简单的工作流
   - 添加"Qwen 文生图"工具
   - 配置测试提示词

2. **运行测试**
   ```
   提示词: 一朵红色的玫瑰花
   模型: Qwen/Qwen-Image
   ```

3. **验证结果**
   - 检查是否成功生成图像
   - 验证图像质量和内容
   - 确认处理时间合理

## 🚨 故障排除

### 常见问题

1. **插件加载失败**
   ```
   错误: 无法加载插件
   解决: 检查 manifest.yaml 格式和依赖安装
   ```

2. **API Key 验证失败**
   ```
   错误: ModelScope API key 格式错误
   解决: 确认 API Key 以 'ms-' 开头且长度正确
   ```

3. **图像生成超时**
   ```
   错误: 图像生成超时（5分钟）
   解决: 检查网络连接，简化提示词，或增加超时时间
   ```

4. **网络连接问题**
   ```
   错误: 网络请求错误
   解决: 检查防火墙设置，确保能访问 api-inference.modelscope.cn
   ```

### 调试模式

启用详细日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 性能优化

1. **内存优化**
   - 及时释放图像数据
   - 避免同时处理多个大图像

2. **网络优化**
   - 使用稳定的网络连接
   - 考虑设置代理（如需要）

## 📊 监控和维护

### 性能指标

- 平均生成时间：30-120秒
- 成功率：>95%
- 内存使用：<100MB

### 定期维护

1. **更新依赖**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **检查 API 限制**
   - 监控 API 调用频率
   - 关注 ModelScope 服务状态

3. **备份配置**
   - 定期备份插件配置
   - 记录重要的配置变更

## 🔗 相关资源

- [ModelScope API 文档](https://modelscope.cn/docs)
- [Dify 插件开发文档](https://docs.dify.ai)
- [问题反馈](https://github.com/your-repo/issues)

---

如有问题，请参考故障排除部分或联系技术支持。