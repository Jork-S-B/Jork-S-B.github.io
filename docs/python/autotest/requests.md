下载大文件

```python
import requests

response = requests.get('http://example.com/largefile.zip', stream=True)

# 检查请求是否成功
if response.status_code == 200:
    # 打开一个本地文件用于写入
    with open('largefile.zip', 'wb') as f:
        # 使用 iter_content 分块读取响应内容
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # 过滤掉 keep-alive 新块
                f.write(chunk)
                # 显示下载进度
                print('.', end='', flush=True)

print("Download complete!")

```