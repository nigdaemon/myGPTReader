import logging
from llama_index.prompts.prompts import QuestionAnswerPrompt

QUESTION_ANSWER_PROMPT_TMPL_CN = (
    "上下文信息如下所示： \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "我的问题是：{query_str}\n 。用中文回答，如果返回是英文，将它翻译为中文。"
)

QUESTION_ANSWER_PROMPT_TMPL_EN = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "My question is {query_str}\n"
)

def get_prompt_template(language='zh'):
    logging.info(f"=====> Get prompt template with language: {language}")
    if language == 'en':
        return QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL_EN)
    else:
        return QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL_CN)