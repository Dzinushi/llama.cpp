import requests
from typing import Dict


class LlamaServerSimpleAPI:
    def __init__(self, url: str = "http://localhost:5002/completion"):
        self.url = url

    def __call__(self, prompt: str) -> Dict:
        data = {
            "prompt": prompt,
            "temperature": 0.1,
            "n_predict": 256,
            "top_p": 0.75,
            "top_k": 40,
        }
        data_revive = {
            "prompt": "!",
            "temperature": 0,
            "n_predict": 1,
        }
        requests.post(url=self.url, json=data_revive)
        response = requests.post(url=self.url, json=data).json()
        return response
