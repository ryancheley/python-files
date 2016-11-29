import glob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread


f = []
for filename in glob.glob('/Users/Ryan/Dropbox/Ryan/**/*', recursive=True):
    f.append(filename.split('/')[-1])

words = ' '
for line in f:
    words= words + line

stopwords = {'https'}

logomask = imread('mask-cloud.png')

wordcloud = WordCloud(
    font_path='/Users/Ryan/Library/Fonts/Inconsolata.otf',
    stopwords=STOPWORDS.union(stopwords),
    #background_color='black',
    background_color='white',
    mask = logomask,
    max_words=1000,
    width=1800,
    height=1400
).generate(words)

plt.imshow(wordcloud.recolor(color_func=None, random_state=3))
plt.axis('off')
plt.savefig('/Users/Ryan/Dropbox/Ryan/Post Images/dropbox_wordcloud.png', dpi=300)
plt.show()

