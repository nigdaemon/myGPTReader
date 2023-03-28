import json
from datetime import date
import logging
import feedparser
import html2text
import concurrent.futures

from app.gpt import get_answer_from_llama_web

with open("app/data/crypto_news_rss.json", "r") as f:
    rss_urls = json.load(f)

TODAY = today = date.today()
MAX_DESCRIPTION_LENGTH = 300
MAX_POSTS = 3


def cut_string(text):
    words = text.split()
    new_text = ""
    count = 0
    for word in words:
        if len(new_text + word) > MAX_DESCRIPTION_LENGTH:
            break
        new_text += word + " "
        count += 1

    return new_text.strip() + '...'

def get_summary_from_gpt_thread(url):
    news_summary_prompt = '请用中文简短概括这篇文章的内容。'
    return str(get_answer_from_llama_web([news_summary_prompt], [url]))

def get_summary_from_gpt(url):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_summary_from_gpt_thread, url)
        return future.result(timeout=300)

def get_description(entry):
    gpt_answer = None
    try:
        gpt_answer = get_summary_from_gpt(entry.link)
    except Exception as e:
        logging.error(e)
    if gpt_answer is not None:
        summary = 'AI: ' + gpt_answer
    else:
        summary = cut_string(get_text_from_html(entry.summary))
    return summary

def get_text_from_html(html):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_tables = False
    text_maker.ignore_images = True
    return text_maker.handle(html)

def get_post_urls_with_title(rss_url):
    feed = feedparser.parse(rss_url)
    updated_posts = []
    
    for entry in feed.entries:
        published_time = entry.published_parsed if 'published_parsed' in entry else None
        # published_date = date(published_time.tm_year,
        #                       published_time.tm_mon, published_time.tm_mday)
        updated_post = {}
        updated_post['title'] = entry.title
        updated_post['summary'] = get_description(entry)
        updated_post['url'] = entry.link
        updated_post['publish_date'] = published_time
        updated_posts.append(updated_post)
        if len(updated_posts) >= MAX_POSTS:
            break
        
    return updated_posts

def build_slack_blocks(title, news):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{title} # {TODAY.strftime('%Y-%m-%d')}"
            }
        }]
    for news_item in news:
        blocks.extend([{
            "type": "section",
            "text": {
				"text": f"*{news_item['title']}*",
				"type": "mrkdwn"
			},
        },{
            "type": "section",
            "text": {
				"text": f"{news_item['summary']}",
				"type": "plain_text"
			},
        },{
            "type": "section",
            "text": {
				"text": f"原文链接：<{news_item['url']}>",
				"type": "mrkdwn"
			},
        },{
            "type": "divider"
        }])
    return blocks

def build_hot_news_blocks(news_key):
    rss = rss_urls[news_key]['rss']['hot']
    hot_news = get_post_urls_with_title(rss['url'])
    hot_news_blocks = build_slack_blocks(
        rss['name'], hot_news)
    return hot_news_blocks

def build_research_hot_news_blocks():
    return build_hot_news_blocks('research')

def build_DeFi_hot_news_blocks():
    return build_hot_news_blocks('DeFi')

def build_web3_hot_news_blocks():
    return build_hot_news_blocks('web3')

def build_lookfor_news_hot_news_blocks():
    return build_hot_news_blocks('lookfor')

def build_cnnews_news_hot_news_blocks():
    return build_hot_news_blocks('cnnews')

def build_allnews_news_hot_news_blocks():
    return build_hot_news_blocks('allnews')

def build_newsletter_news_hot_news_blocks():
    return build_hot_news_blocks('newsletter')

def build_OU_news_hot_news_blocks():
    return build_hot_news_blocks('OU')

def build_program_news_hot_news_blocks():
    return build_hot_news_blocks('program')

def build_FOMO_news_hot_news_blocks():
    return build_hot_news_blocks('FOMO')

def build_all_crypto_block():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        research_news = executor.submit(build_research_hot_news_blocks)
        DeFi_news = executor.submit(build_DeFi_hot_news_blocks)
        web3_news = executor.submit(build_web3_hot_news_blocks)
        lookfor_news = executor.submit(build_lookfor_news_hot_news_blocks)
        cnnews_news = executor.submit(build_cnnews_news_hot_news_blocks)
        allnews_news = executor.submit(build_allnews_news_hot_news_blocks)
        newsletter_news = executor.submit(build_newsletter_news_hot_news_blocks)
        OU_news = executor.submit(build_OU_news_hot_news_blocks)
        program_news = executor.submit(build_program_news_hot_news_blocks)
        FOMO_news = executor.submit(build_FOMO_news_hot_news_blocks)

        research_news_block = research_news.result()
        DeFi_news_block = DeFi_news.result()
        web3_news_block = web3_news.result()
        lookfor_news_block = lookfor_news.result()
        cnnews_news_block = cnnews_news.result()
        allnews_news_block = allnews_news.result()
        newsletter_news_block = newsletter_news.result()
        OU_news_block = OU_news.result()
        program_news_block = program_news.result()
        FOMO_news_block = FOMO_news.result()

        return [research_news_block, DeFi_news_block, web3_news_block,
                           lookfor_news_block, cnnews_news_block, allnews_news_block,
                           newsletter_news_block, OU_news_block, program_news_block, FOMO_news_block]