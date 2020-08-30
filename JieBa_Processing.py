import jieba
import re


def jieba_cut(comments_list):
    print('正在分词中，请稍后......')
    jieba_list = []
    stopwords = stop_words_list()
    for comment in comments_list:
        strings = re.sub(r'[^\w\s]', '', comment.strip())
        cut_list = jieba.lcut(strings, cut_all=False)
        for word in cut_list:
            if word not in stopwords:
                jieba_list.append(word)
    print('分词完成！')
    return jieba_list


def stop_words_list():
    with open('stop_words.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]
