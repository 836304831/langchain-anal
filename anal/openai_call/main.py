"""
@author: acedar
@time: 2023/6/22 11:10
@file: function_call.py
"""

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


proxies = {
  'no_proxy': 'http://127.0.0.1:7890',
  'https': 'http://127.0.0.1:7890',
}

response = openai.Completion.create(
  model="gpt-3.5-turbo",
  prompt="青梅竹马是什么意思",
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"],
  proxies=proxies
)
print(response.json())
