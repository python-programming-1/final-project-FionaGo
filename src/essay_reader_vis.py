from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

text_positive = pd.read_csv('Columbia_Admitted.txt')
text_negative = pd.read_csv('Columbia_Not_Admitted.txt')

wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'black',
    stopwords = STOPWORDS).generate(str(text_negative))

fig = plt.figure(
    figsize = (40, 30),
    facecolor = 'k',
    edgecolor = 'k')
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()