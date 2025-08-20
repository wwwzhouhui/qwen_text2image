#!/usr/bin/env python3
"""
Qwen Text2Image 插件测试脚本
用于在开发环境中测试插件功能
"""

import os
import sys
from tools.text2image import Text2ImageTool

class MockRuntime:
    """模拟运行时环境"""
    def __init__(self, api_key: str):
        self.credentials = {"api_key": api_key}

def test_text2image_tool():
    """测试文生图工具"""
    
    # 从环境变量获取 API Key
    api_key = os.getenv("MODELSCOPE_API_KEY")
    if not api_key:
        print("❌ 请设置环境变量 MODELSCOPE_API_KEY")
        print("   export MODELSCOPE_API_KEY=ms-your-api-key")
        return False
    
    # 验证 API Key 格式
    if not api_key.startswith("ms-"):
        print("❌ API Key 格式错误，应该以 'ms-' 开头")
        return False
    
    print("🚀 开始测试 Qwen Text2Image 插件...")
    print(f"📝 使用 API Key: {api_key[:10]}...")
    
    # 创建工具实例
    tool = Text2ImageTool()
    tool.runtime = MockRuntime(api_key)
    
    # 测试参数
    test_params = {
        "prompt": "一只可爱的橙色小猫坐在绿色的草地上，背景是蓝天白云",
        "model": "Qwen/Qwen-Image"
    }
    
    print(f"🎨 测试提示词: {test_params['prompt']}")
    print(f"🤖 使用模型: {test_params['model']}")
    print("=" * 50)
    
    try:
        # 调用工具
        messages = list(tool._invoke(test_params))
        
        # 输出所有消息
        image_generated = False
        for i, message in enumerate(messages, 1):
            if hasattr(message, 'type'):
                if message.type == 'text':
                    print(f"[{i}] 📄 {message.message}")
                elif message.type == 'blob':
                    print(f"[{i}] 🖼️  图像生成成功！")
                    print(f"     📊 图像大小: {len(message.blob)} 字节")
                    print(f"     📋 MIME 类型: {message.meta.get('mime_type', 'unknown')}")
                    image_generated = True
                    
                    # 保存图像到本地（可选）
                    if message.meta.get('mime_type') == 'image/png':
                        with open('test_output.png', 'wb') as f:
                            f.write(message.blob)
                        print(f"     💾 图像已保存为: test_output.png")
            else:
                print(f"[{i}] ❓ 未知消息类型: {message}")
        
        if image_generated:
            print("\n✅ 测试成功！插件工作正常。")
            return True
        else:
            print("\n❌ 测试失败：未生成图像。")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔧 Qwen Text2Image 插件测试工具")
    print("=" * 50)
    
    # 检查依赖
    try:
        import requests
        import PIL
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return
    
    # 运行测试
    success = test_text2image_tool()
    
    if success:
        print("\n🎉 所有测试通过！插件可以正常使用。")
        print("\n📋 下一步:")
        print("1. 将插件部署到 Dify 环境")
        print("2. 在 Dify 中配置 ModelScope API Key")
        print("3. 在工作流中使用文生图工具")
    else:
        print("\n💡 故障排除建议:")
        print("1. 检查网络连接是否正常")
        print("2. 验证 ModelScope API Key 是否有效")
        print("3. 确认 API Key 有图像生成权限")
        print("4. 查看详细错误信息进行调试")

if __name__ == "__main__":
    main()