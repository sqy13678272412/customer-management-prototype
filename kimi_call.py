import json
import os
import sys
from urllib import request, error


API_BASE_URL = os.getenv("KIMI_API_BASE_URL", "https://api.moonshot.cn/v1/chat/completions")
MODEL = os.getenv("KIMI_MODEL", "moonshot-v1-8k")
API_KEY = os.getenv("KIMI_API_KEY")


def call_kimi(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError("请先设置环境变量 KIMI_API_KEY")

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        API_BASE_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as response:
            body = response.read().decode("utf-8")
            result = json.loads(body)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Kimi 请求失败: {exc.code} {detail}") from exc

    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Kimi 返回格式异常: {result}") from exc


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "你好，请用简短中文回复。"
    print(call_kimi(prompt))
