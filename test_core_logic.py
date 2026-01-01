#!/usr/bin/env python3
"""
独立测试脚本 - 测试核心图像生成逻辑
不依赖 dify_plugin，直接测试 ModelScope API 调用
"""

import requests
import time
import json
import os
from PIL import Image
from io import BytesIO

def test_modelscope_api():
    """测试 ModelScope API 的核心逻辑（基于 qwen-image.py）"""
    
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
    
    print("🔧 ModelScope API 核心逻辑测试")
    print("=" * 50)
    print(f"📝 使用 API Key: {api_key[:10]}...")
    
    # API 配置（完全按照 qwen-image.py）
    base_url = 'https://api-inference.modelscope.cn/'
    common_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # 测试参数
    prompt = "一只可爱的橙色小猫坐在绿色的草地上，背景是蓝天白云"
    model = "Qwen/Qwen-Image-2512"
    
    print(f"🎨 测试提示词: {prompt}")
    print(f"🤖 使用模型: {model}")
    print("=" * 50)
    
    try:
        print("🚀 正在提交图像生成任务...")
        
        # 1. 提交异步生成任务（完全按照 qwen-image.py）
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps({
                "model": model,
                "prompt": prompt
            }, ensure_ascii=False).encode('utf-8')
        )
        
        print(f"📡 请求状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"📄 响应内容: {response.text}")
            return False
        
        response.raise_for_status()
        response_data = response.json()
        task_id = response_data.get("task_id")
        
        if not task_id:
            print("❌ 创建任务失败，未获取到任务ID")
            print(f"📄 响应数据: {response_data}")
            return False
        
        print(f"✅ 任务已创建，ID: {task_id}")
        print("⏳ 正在生成图像，请稍候...")
        
        # 2. 轮询任务状态（完全按照 qwen-image.py）
        max_retries = 60  # 最大重试次数（5分钟）
        retry_count = 0
        
        while retry_count < max_retries:
            # 等待 5 秒再查询
            time.sleep(5)
            
            print(f"🔍 查询任务状态 (第 {retry_count + 1} 次)...")
            
            # 查询任务状态
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            
            if result.status_code != 200:
                print(f"❌ 查询状态失败: {result.status_code}")
                print(f"📄 响应内容: {result.text}")
                return False
            
            result.raise_for_status()
            data = result.json()
            
            task_status = data.get("task_status")
            print(f"📊 任务状态: {task_status}")
            
            if task_status == "SUCCEED":
                # 任务成功，下载图像
                output_images = data.get("output_images", [])
                if not output_images:
                    print("❌ 生成成功但未找到图像数据")
                    print(f"📄 响应数据: {data}")
                    return False
                
                image_url = output_images[0]
                print(f"🎨 图像生成成功！")
                print(f"🔗 图像URL: {image_url}")
                print("📥 正在下载图像...")
                
                # 下载图像（按照 qwen-image.py 的方式）
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                
                print(f"📊 图像大小: {len(image_response.content)} 字节")
                
                # 处理图像数据（使用 PIL，与 qwen-image.py 一致）
                image = Image.open(BytesIO(image_response.content))
                print(f"🖼️  图像尺寸: {image.size}")
                print(f"🎨 图像格式: {image.format}")
                print(f"🌈 图像模式: {image.mode}")
                
                # 保存图像
                output_filename = "test_output.jpg"
                image.save(output_filename)
                print(f"💾 图像已保存为: {output_filename}")
                
                print("\n🎉 测试成功！核心逻辑工作正常。")
                return True
                
            elif task_status == "FAILED":
                error_info = data.get("error", {})
                error_message = error_info.get("message", "未知错误")
                print(f"❌ 图像生成失败: {error_message}")
                print(f"📄 完整错误信息: {data}")
                return False
            
            # 继续等待
            wait_time = (retry_count + 1) * 5
            print(f"⏳ 图像正在生成中，已等待 {wait_time} 秒...")
            retry_count += 1
        
        # 超时处理
        print("⏰ 图像生成超时（5分钟），请稍后再试")
        return False
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ API Key 无效，请检查您的 ModelScope API Key")
        elif e.response.status_code == 429:
            print("❌ API 调用频率过高，请稍后再试")
        else:
            print(f"❌ HTTP 错误: {e.response.status_code} - {str(e)}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {str(e)}")
        return False
    except KeyError as e:
        print(f"❌ API 响应格式错误，缺少字段: {str(e)}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ API 响应解析错误: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 生成图像时出现未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔧 Qwen Text2Image 核心逻辑测试工具")
    print("基于 qwen-image.py 的实现逻辑")
    print("=" * 50)
    
    # 检查依赖
    try:
        import requests
        import PIL
        print("✅ 依赖检查通过 (requests, PIL)")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install requests Pillow")
        return
    
    # 运行测试
    success = test_modelscope_api()
    
    if success:
        print("\n🎉 核心逻辑测试通过！")
        print("\n📋 测试结果:")
        print("✅ ModelScope API 连接正常")
        print("✅ 异步任务提交成功")
        print("✅ 任务状态轮询正常")
        print("✅ 图像下载和处理成功")
        print("✅ 与 qwen-image.py 逻辑一致")
        
        print("\n📋 下一步:")
        print("1. 核心逻辑验证完成")
        print("2. 可以安全部署到 Dify 环境")
        print("3. 在 Dify 中配置相同的 API Key")
    else:
        print("\n💡 故障排除建议:")
        print("1. 检查网络连接是否正常")
        print("2. 验证 ModelScope API Key 是否有效")
        print("3. 确认 API Key 有图像生成权限")
        print("4. 检查是否能访问 api-inference.modelscope.cn")
        print("5. 查看上方的详细错误信息")

if __name__ == "__main__":
    main()