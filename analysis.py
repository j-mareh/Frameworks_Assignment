import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load dataset
df = pd.read_csv("metadata.csv")

# Clean
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# Publications by year
year_counts = df['year'].value_counts().sort_index()
plt.bar(year_counts.index, year_counts.values)
plt.title("Publications by Year")
plt.show()

# Top journals
top_journals = df['journal'].value_counts().head(10)
sns.barplot(x=top_journals.values, y=top_journals.index)
plt.title("Top Journals")
plt.show()
