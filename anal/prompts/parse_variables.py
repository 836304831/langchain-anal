# -*- coding: utf-8 -*-
# ----------------------------
# @Time    : 2023/7/15 11:10
# @Author  : acedar
# @FileName: parse_variables.py
# ----------------------------

from jinja2 import Environment, meta
from string import Formatter


def variables_from_template(template, **kwargs):
    if "template_format" in kwargs and kwargs["template_format"] == "jinja2":
        # Get the variables for the template
        env = Environment()
        ast = env.parse(template)
        variables = meta.find_undeclared_variables(ast)
    else:
        variables = {
            v for _, v, _, _ in Formatter().parse(template) if v is not None
        }
    return variables


template_string = """Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text: ```{text}```
"""

variables = variables_from_template(template_string)

print(variables)
