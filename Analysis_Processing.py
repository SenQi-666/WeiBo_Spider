from MySQL_Control import MySQLClient
from matplotlib import pyplot as plt
from snownlp import SnowNLP
import numpy as np


def emotion_analysis(comments_list):
    print('正在进行情感分析，请稍后......')
    sentiments_list = []
    for comment in comments_list:
        if len(comment) == 0:
            continue
        else:
            s = SnowNLP(comment)
            sentiments_list.append(s.sentiments)
    plt.hist(sentiments_list, bins=np.arange(0, 1, 0.02))
    plt.xlabel('Number of People')
    plt.ylabel('Emotional Points')
    plt.title('The Chart Of Emotional Analysis')
    plt.savefig('EmotionAnalysis.png')
    print('情感分析完成！')


if __name__ == '__main__':
    emotion_analysis(MySQLClient().show())
