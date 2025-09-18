import re
import requests
import time
import json
from collections.abc import Generator
from PIL import Image
from io import BytesIO
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin import Tool

class Text2ImageTool(Tool):
    def _invoke(
        self, tool_parameters: dict
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        基于 ModelScope API 的异步文生图工具
        实现逻辑完全参考 qwen-image.py
        
        Args:
            tool_parameters: 工具参数字典，包含 prompt 和 model
            
        Yields:
            ToolInvokeMessage: 工具调用消息，包括进度反馈和最终图像结果
        """
        # 1. 获取 API 配置
        api_key = self.runtime.credentials.get("api_key")
        base_url = 'https://api-inference.modelscope.cn/'
        
        # 2. 获取和验证参数
        prompt = tool_parameters.get("prompt", "")
        if not prompt:
            yield self.create_text_message("❌ 请输入提示词")
            return

        size = tool_parameters.get("size", "1024x1024")
        if re.match(r"^\d+x\d+$", size) is None:
            yield self.create_text_message("❌ 尺寸参数格式错误，请使用 WxH 格式")
            yield self.create_text_message("💡 使用默认尺寸: 1024x1024")
            size = "1024x1024"

        model = tool_parameters.get("model", "Qwen/Qwen-Image")
        
        # 3. 设置请求头（完全按照 qwen-image.py 的格式）
        common_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            yield self.create_text_message("🚀 正在提交图像生成任务...")
            
            # 添加调试信息
            yield self.create_text_message(f"🔧 使用模型: {model}")
            yield self.create_text_message(f"🔧 提示词长度: {len(prompt)} 字符")
            
            # 4. 提交异步生成任务（完全按照 qwen-image.py 的实现）
            request_data = {
                "model": model,
                "prompt": prompt,
                "n": 1,  # 添加生成图片数量参数
                "size": size  # 添加图片尺寸参数
            }
            
            response = requests.post(
                f"{base_url}v1/images/generations",
                headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
                json=request_data,  # 使用 json 参数而不是手动编码
                timeout=30  # 添加超时设置
            )
            
            # 检查响应状态
            if response.status_code != 200:
                yield self.create_text_message(f"🔧 API 响应状态码: {response.status_code}")
                yield self.create_text_message(f"🔧 响应内容: {response.text[:500]}")
            
            response.raise_for_status()
            
            # 获取任务 ID
            response_data = response.json()
            task_id = response_data.get("task_id")
            
            if not task_id:
                yield self.create_text_message("❌ 创建任务失败，未获取到任务ID")
                return
            
            yield self.create_text_message(f"✅ 任务已创建，ID: {task_id}")
            yield self.create_text_message("⏳ 正在生成图像，请稍候...")
            
            # 5. 轮询任务状态（完全按照 qwen-image.py 的实现）
            max_retries = 60  # 最大重试次数，防止无限等待（5分钟）
            retry_count = 0
            
            while retry_count < max_retries:
                # 等待 5 秒再查询（与 qwen-image.py 保持一致）
                time.sleep(5)
                
                # 查询任务状态
                result = requests.get(
                    f"{base_url}v1/tasks/{task_id}",
                    headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                )
                
                result.raise_for_status()
                data = result.json()
                
                task_status = data.get("task_status")
                
                if task_status == "SUCCEED":
                    # 任务成功，下载图像（按照 qwen-image.py 的处理方式）
                    output_images = data.get("output_images", [])
                    if not output_images:
                        yield self.create_text_message("❌ 生成成功但未找到图像数据")
                        return
                    
                    image_url = output_images[0]
                    yield self.create_text_message("🎨 图像生成成功，正在下载...")
                    
                    # 下载图像（完全按照 qwen-image.py 的方式）
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                    
                    # 处理图像数据（使用 PIL，与 qwen-image.py 一致）
                    image = Image.open(BytesIO(image_response.content))
                    
                    # 将图像转换为字节流
                    img_byte_arr = BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    # 返回图像
                    yield self.create_blob_message(
                        blob=img_byte_arr,
                        meta={"mime_type": "image/png"}
                    )
                    yield self.create_text_message("🎉 图像生成完成！")
                    return
                    
                elif task_status == "FAILED":
                    error_info = data.get("error", {})
                    error_message = error_info.get("message", "未知错误")
                    yield self.create_text_message(f"❌ 图像生成失败: {error_message}")
                    return
                
                # 继续等待，提供进度反馈
                wait_time = (retry_count + 1) * 5
                yield self.create_text_message(
                    f"⏳ 图像正在生成中，已等待 {wait_time} 秒..."
                )
                retry_count += 1
            
            # 超时处理
            yield self.create_text_message("⏰ 图像生成超时（5分钟），请稍后再试")
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                yield self.create_text_message("❌ API Key 无效，请检查您的 ModelScope API Key")
            elif e.response.status_code == 429:
                yield self.create_text_message("❌ API 调用频率过高，请稍后再试")
            elif e.response.status_code == 500:
                yield self.create_text_message("❌ ModelScope 服务器内部错误")
                yield self.create_text_message("💡 可能的解决方案:")
                yield self.create_text_message("1. 检查提示词是否包含敏感内容")
                yield self.create_text_message("2. 尝试简化提示词描述")
                yield self.create_text_message("3. 稍后重试，可能是服务器临时故障")
                yield self.create_text_message(f"🔧 错误详情: {e.response.text[:200] if hasattr(e.response, 'text') else 'N/A'}")
            else:
                yield self.create_text_message(f"❌ HTTP 错误: {e.response.status_code} - {str(e)}")
                if hasattr(e.response, 'text'):
                    yield self.create_text_message(f"🔧 响应内容: {e.response.text[:200]}")
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"❌ 网络请求错误: {str(e)}")
        except KeyError as e:
            yield self.create_text_message(f"❌ API 响应格式错误，缺少字段: {str(e)}")
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"❌ API 响应解析错误: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"❌ 生成图像时出现未知错误: {str(e)}")