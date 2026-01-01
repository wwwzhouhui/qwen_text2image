#!/usr/bin/env python3
import requests
import time
import json
import os
from PIL import Image
from io import BytesIO

def verify_image2image():
    """验证图生图核心逻辑"""
    
    # 1. 配置
    api_key = os.getenv("MODELSCOPE_API_KEY")
    if not api_key:
        print("❌ 请设置环境变量 MODELSCOPE_API_KEY")
        return
        
    base_url = 'https://api-inference.modelscope.cn/'
    common_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # 2. 准备测试数据
    # 使用官方推荐的公开图片 URL 进行验证
    public_url = "https://modelscope.oss-cn-beijing.aliyuncs.com/Dog.png"
    prompt = "给图中的狗戴上一个生日帽"
    model = "Qwen/Qwen-Image-Edit-2511"
    
    print(f"🚀 开始验证图生图功能...")
    print(f"🤖 模型: {model}")
    print(f"🖼️ 使用公开图片: {public_url}")
    print(f"📝 提示词: {prompt}")
    
    # 3. 提交任务
    request_data = {
        "model": model,
        "prompt": prompt,
        "image_url": [public_url]
    }
    
    try:
        print("\n📡 正在提交任务...")
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps(request_data, ensure_ascii=False).encode('utf-8'),
            timeout=30
        )
        response.raise_for_status()
        task_id = response.json().get("task_id")
        print(f"✅ 任务提交成功，ID: {task_id}")
        
        # 4. 轮询结果
        print("⏳ 正在等待生成结果 (每5秒检查一次)...")
        while True:
            result = requests.get(
                f"{base_url}v1/tasks/{task_id}",
                headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            result.raise_for_status()
            data = result.json()
            status = data.get("task_status")
            
            if status == "SUCCEED":
                print("\n🎉 任务执行成功！")
                img_url = data.get("output_images", [None])[0]
                if img_url:
                    print(f"🔗 结果图片地址: {img_url}")
                    # 下载并保存
                    img_data = requests.get(img_url).content
                    image = Image.open(BytesIO(img_data))
                    image.save("verify_result.png")
                    print("💾 结果已保存为 verify_result.png")
                else:
                    print("⚠️ 任务成功但未找到图片地址。")
                break
            elif status == "FAILED":
                print("\n❌ 任务失败！")
                print(f"🔍 完整响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                break
            
            print(f"  > 当前状态: {status}...")
            time.sleep(5)
            
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    verify_image2image()
