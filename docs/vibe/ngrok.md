在没有服务器的情况下，可以使用以下免费方案来测试飞书机器人应用的交互功能：

## ngrok（推荐）
ngrok 是最简单、最常用的内网穿透工具，可以将本地服务暴露到公网。

**使用步骤：**

1. **注册 ngrok 账号**
   - 访问 https://ngrok.com/
   - 注册免费账号
   - 获取 Authtoken

2. **安装 ngrok**
   ```bash
   # Windows (使用 PowerShell)
   choco install ngrok
   
   # 或手动下载
   # 访问 https://ngrok.com/download 下载 Windows 版本
   ```

3. **配置 ngrok**
   ```bash
   ngrok config add-authtoken your_authtoken_here
   ```

4. **启动 ngrok**
   ```bash
   ngrok http 8100
   ```
   
   运行后会显示类似：
   ```
   Forwarding: https://1234-567-890-123.ngrok-free.app -> http://localhost:8100
   ```

5. **配置飞书回调地址**
   - 将 `https://1234-567-890-123.ngrok-free.app/callback` 填入飞书机器人的回调地址

6. **启动项目**
   ```bash
   python run.py
   ```

**优点：**
- 完全免费
- 使用简单
- 支持 HTTPS
- 无需域名

**缺点：**
- 免费版每次重启 ngrok 会更换域名（需要重新配置飞书）
- 有连接数限制

## 飞书机器人配置

1. 创建企业应用机器人，设置权限，主要包括收发群/私聊消息
2. 设置事件配置，包括请求回调地址、接收消息的事件
3. 设置回调配置，包括请求回调地址、交互方式如卡片
4. 可选，设置加密策略，主要是Verification Token

20260320：回调消息需要有challenge字段，如下

```python
   # 处理飞书 Challenge 验证（配置回调URL时使用）
   if 'challenge' in data:
       return {"challenge": data['challenge']}
```
     