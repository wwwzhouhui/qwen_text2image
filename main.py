from dify_plugin import Plugin, DifyPluginEnv

# 配置插件环境，设置超时时间为 300 秒（5分钟）以适应图像生成的时间需求
plugin = Plugin(DifyPluginEnv(MAX_REQUEST_TIMEOUT=300))

if __name__ == '__main__':
    plugin.run()