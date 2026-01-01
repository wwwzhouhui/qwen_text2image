"""
测试 litterbox.catbox.moe 临时图床是否可用
"""
import requests
from PIL import Image
from io import BytesIO


def upload_to_catbox(image_bytes: bytes, filename: str = "image.png") -> str:
    """
    上传图像到 litterbox.catbox.moe（临时图床，1小时后过期）
    返回公开可访问的 URL
    """
    url = "https://litterbox.catbox.moe/resources/internals/api.php"
    files = {
        'fileToUpload': (filename, image_bytes, 'image/png')
    }
    data = {
        'reqtype': 'fileupload',
        'time': '1h'  # 临时存储 1 小时
    }

    response = requests.post(url, files=files, data=data, timeout=60)
    response.raise_for_status()

    result_url = response.text.strip()
    if result_url.startswith('http'):
        return result_url
    else:
        raise Exception(f"图床上传失败: {result_url}")


def test_catbox():
    print("=" * 50)
    print("测试 litterbox.catbox.moe 临时图床")
    print("=" * 50)

    # 1. 创建一个简单的测试图像
    print("\n1. 创建测试图像...")
    image = Image.new('RGB', (200, 200), color='blue')
    # 添加一些简单的图案
    for x in range(50, 150):
        for y in range(50, 150):
            image.putpixel((x, y), (255, 0, 0))  # 红色方块

    # 转换为字节
    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG')
    image_bytes = img_buffer.getvalue()
    print(f"   图像大小: {len(image_bytes)} 字节")

    # 2. 上传到图床
    print("\n2. 上传到临时图床...")
    try:
        public_url = upload_to_catbox(image_bytes, "test_image.png")
        print(f"   ✅ 上传成功!")
        print(f"   公开 URL: {public_url}")
    except Exception as e:
        print(f"   ❌ 上传失败: {e}")
        return False

    # 3. 验证 URL 是否可访问
    print("\n3. 验证 URL 是否可访问...")
    try:
        response = requests.get(public_url, timeout=30)
        response.raise_for_status()
        print(f"   ✅ URL 可访问!")
        print(f"   响应状态码: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"   内容大小: {len(response.content)} 字节")

        # 验证是否是有效图像
        downloaded_image = Image.open(BytesIO(response.content))
        print(f"   图像尺寸: {downloaded_image.size}")
        print(f"   图像模式: {downloaded_image.mode}")
    except Exception as e:
        print(f"   ❌ 访问失败: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ 临时图床测试通过!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    test_catbox()
