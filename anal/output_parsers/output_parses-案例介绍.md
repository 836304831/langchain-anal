
# output_parses代码解析知识点汇总

## 解析的格式种类

- json格式的字符串解析
- bool类型的结果解析
- list结果的解析
- 时间的解析
- 类对象的解析
- 基于上述基本类型的组合, 比如重试中的解析，多个数据结构组合


## 工具介绍
在output_parse模块中，使用到了第三方包，Pydantic和Guardrails，先大致了解一下这个包是什么。
### Pydantic是什么
    Pydantic 是一个Python 库，它提供了一种简单方便的方法来验证和操作数据。 
    它的创建是为了帮助简化数据验证过程并提高开发人员的效率。 
    Pydantic 与Python 的数据结构无缝集成，并提供灵活且用户友好的API 来定义和验证数据。
    from pydantic import BaseModel
    class Person(BaseModel):
        name: str
    
    p = {"name": "Tom"}
    p = Person(**p)
    print(p.json()) # {"name": "Tom"}
    
    Person(person="Tom")  # 报错, 参数不是name

### Guardrails是什么

    Guardrails 是一个 Python 包，可让用户为大型语言模型 (LLM) 的输出添加结构、类型和质量保证。护栏：
    对 LLM 输出进行 pydantic 式验证。这包括语义验证，例如检查生成文本中的偏差、检查生成代码中的错误等。
    当验证失败时采取纠正措施（例如重新询问LLM），
    强制执行结构和类型保证（例如 JSON）
    安装方式： pip install guardrails-ai)

## output_parse案例演示

### boolean值输出解析
```python
# 1.模板定义
question = """\
1+1=2, 正确么，请回答：
{answer_format}
"""
answer_format = "YES or no"

from langchain.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_template(question)
print(prompt_template)
# 输出: input_variables=['answer_format'] output_parser=None partial_variables={} messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['answer_format'], output_parser=None, partial_variables={}, template='1+1=2, 正确么，请回答：\n{answer_format}\n', template_format='f-string', validate_template=True), additional_kwargs={})]

# 2.模板信息填充
messages = prompt_template.format_messages(answer_format=answer_format)

# 3.模型定义
from langchain.chat_models.openai import ChatOpenAI
chat = ChatOpenAI(temperature=0.0)
response = chat(messages)
print(response.content)
print(type(response.content))
# 输出：
# YES
# <class 'str'>

# 4. 模型输出结果解析
from langchain.output_parsers import BooleanOutputParser
output_parser = BooleanOutputParser()
output = output_parser.parse(response.content)
print(type(output))
print(output)
# 输出
# <class 'bool'>
# True
```

### pydannic的使用
```python
# 1.解析结构定义, field定义
from pydantic import BaseModel, Field
class Answer(BaseModel):
    ans: str = Field(description="给出计算结果")

# 2.结构解析模板生成
from langchain.output_parsers import PydanticOutputParser
output_parser = PydanticOutputParser(pydantic_object=Answer)
print(output_parser.get_format_instructions())
# 输出：The output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{"properties": {"ans": {"title": "Ans", "description": "\\u7ed9\\u51fa\\u8ba1\\u7b97\\u7ed3\\u679c", "type": "string"}}, "required": ["ans"]}\n```

# 3. 模板定义
question = """\
你是一个计算机，{format_instructions}：
```{query}``` 的结果
"""
query = "20+30"
from langchain.prompts import ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template(question)
print(prompt_template)
# 输出：input_variables=['format_instructions', 'query'] output_parser=None partial_variables={} messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['format_instructions', 'query'], output_parser=None, partial_variables={}, template='你是一个计算机，{format_instructions}：\n```{query}``` 的结果\n', template_format='f-string', validate_template=True), additional_kwargs={})]
messages = prompt_template.format_messages(query=query, format_instructions=output_parser.get_format_instructions())

# 4. 模型定义
from langchain.chat_models.openai import ChatOpenAI
chat = ChatOpenAI(temperature=0.0)
response = chat(messages)
print(response.content)
print(type(response.content))
# 输出
# {"ans": "50"}
# <class 'str'>

# 5. 类结构解析
output = output_parser.parse(response.content)
print(output)
# 输出: Answer(ans='50')
```
