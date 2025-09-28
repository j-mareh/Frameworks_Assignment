import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df = df.dropna(subset=["title", "publish_time"]).copy()
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = df["publish_time"].dt.year
    return df

df = load_data()

# App title and description
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers from the CORD-19 dataset")

# Sidebar controls
year_range = st.slider("Select publication year range", 
                       int(df["year"].min()), int(df["year"].max()), 
                       (2020, 2021))

filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

st.write(f"Showing {len(filtered_df)} papers published between {year_range[0]} and {year_range[1]}.")

# Visualization: Publications per year
st.subheader("Publications Over Time")
year_counts = filtered_df["year"].value_counts().sort_index()

fig, ax = plt.subplots()
sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax, color="skyblue")
ax.set_title("Publications by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
st.pyplot(fig)

# Visualization: Top Journals
st.subheader("Top Journals")
top_journals = filtered_df["journal"].value_counts().head(10)

fig, ax = plt.subplots()
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax, palette="viridis")
ax.set_title("Top Journals")
st.pyplot(fig)

# Visualization: Word Cloud of Titles
st.subheader("Word Cloud of Titles")
title_text = " ".join(filtered_df["title"].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(title_text)

fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Show sample data
st.subheader("Sample Data")
st.dataframe(filtered_df.head(20))
