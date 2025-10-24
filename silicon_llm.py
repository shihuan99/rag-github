import json
import os
from typing import Iterator

import env

from llama_index.core.llms import CustomLLM
from llama_index.core.base.llms.types import LLMMetadata, CompletionResponse
import requests

# 硅基流动LLM接口适配
class SiliconFlowLLM(CustomLLM):
    def __init__(self):
        super().__init__()

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=4096,  # 根据实际模型调整
            num_output=1024,
            model_name="silicon-flow-model"
        )

    def stream_complete(self, prompt: str, **kwargs):
        def empty_generator() -> Iterator[CompletionResponse]:
            yield CompletionResponse(text="")
        return empty_generator()

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        headers = {
            "Authorization": f"Bearer {os.environ['API_KEY']}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "Qwen/Qwen2-7B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        response = requests.post(
            f"https://api.siliconflow.cn/v1/chat/completions",
            headers=headers,
            json=data,
            proxies=env.proxies,
            verify=False
        )
        response.raise_for_status()

        result = response.json()
        text = result["choices"][0]["message"]["content"]

        return CompletionResponse(text=text)