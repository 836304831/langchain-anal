
# chains说明
chains对组件的一系列调用，因为在很多场景下，一个完成的功能需要拆分成多个组件调用，将多个组件组合在一起形成完整的pipleline。
组件的调用可以理解为是单个功能的实现，可以保证功能的灵活性，在很多的通用场景下都能使用，有利于功能的复用。
chains的调用，以完整任务为单位，贴合实际应用。
chains模块的功能整体分为两部分: 
- 一部分是单个功能实现的chain，是对llm和prompt的封装。
- 另一部分是将每个chains组合在一起，形成一个完整的pipeline。

## chains模块介绍
- LLMChain: 对大模型调用的功能，输出内容和格式由用户输入指定
- TransformChain: 对chains之间的输入和输出进行处理，便于chains之间进行数据传输。支持自定义的转换函数。
- OpenAIModerationChain: 通过审核端点传递输入
- MapReduceChain: 将大文档拆分，拆分的每一部分发送给发送到LLM，然后将结果组合返回。
- LLMRequestsChain: 解析url中的结果，获取对应结果发送给LLM

### LLMChain使用例子
```python
from langchain import PromptTemplate, OpenAI, LLMChain

prompt_template = "列举5个描述场景 {scene} 特点的词"
prompt = PromptTemplate(
    input_variables=["scene"],
    template=prompt_template
)


llm = OpenAI(temperature=0)

# 核心要素： 模型，prompt模板
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt
)

print(llm_chain.input_keys)

# 调用call方法
# 返回输入和输出
output = llm_chain({"scene": "长江"})
print(output)

output = llm_chain.run({"scene": "矿泉水"})
print(output)

# 参数指定，只返回输出
output = llm_chain({"scene": "公园"}, return_only_outputs=True)
print(output)
# 参数指定，只返回输出, 不使用字典方式输入(对后续chain是有影响的)
# output = llm_chain("书包", return_only_outputs=True)
# print(output)

# apply方法: 多输入
input_list = [
    {"scene": "房子"},
    {"scene": "图书馆"}
]
# llm_chain.apply(input_list)
```
### TransformChain使用例子
```python

from langchain.chains import TransformChain, LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import json

# transformer chain
def select_feature(inputs):
    print("inputs:", inputs)
    feature_str = inputs["multi_feature"]
    single_feature = feature_str.split("*$*")[0]
    return {"single_feature": single_feature}

transfor_chain = TransformChain(
    input_variables=["multi_feature"], 
    output_variables=["single_feature"],
    transform=select_feature,)

output = transfor_chain({'scene': '白云', 'multi_feature': '云朵*$*柔和*$*悠扬'}, return_only_outputs=True)
print(output)
```

## chains pipeline介绍
- SimpleSequentialChain: 每个步骤都有一个单一的输入/输出，并且一个步骤的输出是下一步的输入
- SequentialChain: 多输入输出的顺序链, 难点: 多输入多输出，如何进行变量的映射。上一个链的多输出，如何精准的传递给下一个链

### SimpleSequentialChain 完整功能使用列子
```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

llm = OpenAI(temperature=0)
template = """ 你是一名小学语文老师，给定一个场景, 使用2-3个词描述其特点：
场景: {scene}
场景特点: """
prompt_template = PromptTemplate(input_variables=["scene"], template=template)
scene_chain = LLMChain(llm=llm, prompt=prompt_template)

llm = OpenAI(temperature=.7)
template = """你是一名小学语文老师，根据给定场景的特点，请造句，要求使用这些场景特点的词,
特点：{feature}
造句结果: """
prompt_template = PromptTemplate(input_variables=["feature"], template=template)
sentence_chain = LLMChain(llm=llm, prompt=prompt_template)

overall_chain = SimpleSequentialChain(chains=[scene_chain, sentence_chain], verbose=True)
review = overall_chain.run("沙滩")
```

### SequentialChain使用例子
```python
llm = OpenAI(temperature=.7)
template = """ 你是一名小学语文老师，给定一个场景, 使用2-3个词描述其特点：
场景: {scene}
场景特点: """
prompt_template = PromptTemplate(input_variables=["scene"], template=template)
scene_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="feature")

llm = OpenAI(temperature=.7)
template = """你是一名小学语文老师，根据给定场景的特点，请造句，要求使用这些场景特点的词,
特点：{feature}
造句结果: """
prompt_template = PromptTemplate(input_variables=["feature"], template=template)
sentence_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="sentence")

llm = OpenAI(temperature=.7)
template = """你是一名小学语文老师，根据给定场景的特点，一次给出这些特点词的反义词,
特点：{feature}
反义词为: """
prompt_template = PromptTemplate(input_variables=["feature"], template=template)
antonym_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="antonym")


from langchain.chains import SequentialChain

overall_chain = SequentialChain(
    chains=[scene_chain, sentence_chain, antonym_chain],
    input_variables=["scene"],
    # Here we return multiple variables
    output_variables=["feature", "sentence", "antonym"],
    verbose=True)
overall_chain({"scene":"白云"})
```

### 带有转换链的pipeline例子
```python
from langchain.chains import TransformChain, LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import json

# first chain
llm = OpenAI(temperature=.7)
template = """ 你是一名小学语文老师，给定一个场景, 使用2-3个词描述其特点, 词时间使用*$*分割：
场景: {scene}
场景特点: """
prompt_template = PromptTemplate(input_variables=["scene"], template=template)
scene_chain = LLMChain(llm=llm, prompt=prompt_template, 
                          output_key="multi_feature")


# transformer chain
def select_feature(inputs):
    print("inputs:", inputs)
    feature_str = inputs["multi_feature"]
    single_feature = feature_str.split("*$*")[0]
    return {"single_feature": single_feature}

transfor_chain = TransformChain(
    input_variables=["multi_feature"], 
    output_variables=["single_feature"],
    transform=select_feature,)

# third chain
template = """你是一名小学语文老师，根据给定场景的特点造句，
特点：{single_feature}
造句结果: """
prompt_template = PromptTemplate(input_variables=["single_feature"], template=template)
llm = OpenAI(temperature=.7)


sentence_chain = LLMChain(llm=llm, prompt=prompt_template, 
                          output_key="sentence")

from langchain.chains import SequentialChain

overall_chain = SequentialChain(
    chains=[scene_chain, transfor_chain, sentence_chain],
    input_variables=["scene"],
    # Here we return multiple variables
    output_variables=["multi_feature", "single_feature", "sentence"],
    verbose=True)
overall_chain({"scene":"白云"})
```
