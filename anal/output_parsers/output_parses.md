
# output_parses代码解析知识点汇总

## 解析的格式种类

- json格式的字符串解析
- bool类型的结果解析
- list结果的解析
- 时间的解析
- 类对象的解析
- 基于上述基本类型的组合, 比如重试中的解析，多个数据结构组合



## Pydantic是什么
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

## Guardrails是什么

    Guardrails 是一个 Python 包，可让用户为大型语言模型 (LLM) 的输出添加结构、类型和质量保证。护栏：
    对 LLM 输出进行 pydantic 式验证。这包括语义验证，例如检查生成文本中的偏差、检查生成代码中的错误等。
    当验证失败时采取纠正措施（例如重新询问LLM），
    强制执行结构和类型保证（例如 JSON）
    安装方式： pip install guardrails-ai)
