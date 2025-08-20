from typing import Any
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.text2image import Text2ImageTool
from dify_plugin import ToolProvider

class ModelScopeProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证 ModelScope API 凭据有效性
        
        Args:
            credentials: 包含 ModelScope API key 的字典
            
        Raises:
            ToolProviderCredentialValidationError: 当凭据验证失败时
        """
        try:
            # 检查 API key 格式
            api_key = credentials.get("api_key")
            if not api_key:
                raise ToolProviderCredentialValidationError(
                    "ModelScope API key 不能为空"
                )
            
            if not api_key.startswith("ms-"):
                raise ToolProviderCredentialValidationError(
                    "无效的 ModelScope API key 格式。应该以 'ms-' 开头"
                )
            
            # 检查 API key 长度（ModelScope API key 通常有固定长度）
            if len(api_key) < 10:
                raise ToolProviderCredentialValidationError(
                    "ModelScope API key 长度不正确"
                )
            
            # 这里可以添加更详细的验证逻辑，比如发送一个测试请求
            # 但为了避免不必要的 API 调用，我们只进行格式验证
            
        except ToolProviderCredentialValidationError:
            # 重新抛出已知的验证错误
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"ModelScope API 凭据验证失败: {str(e)}"
            )