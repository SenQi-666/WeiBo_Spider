from JieBa_Processing import jieba_cut
from MySQL_Control import MySQLClient
from wordcloud import WordCloud


def word_cloud(jieba_list):
    print('正在制作词云，请稍后......')
    wc_string = ' '.join(jieba_list)
    my_wordcloud = WordCloud(
        width=1000,
        height=700,
        background_color='white',
        font_path='/System/Library/fonts/PingFang.ttc',
        scale=4,
        margin=2
    ).generate(wc_string)
    my_wordcloud.to_file('wordcloud.png')
    print('词云制作完成！')


if __name__ == '__main__':
    word_cloud(jieba_cut(MySQLClient().show()))