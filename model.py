import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

os.makedirs("models", exist_ok=True)

df = pd.read_csv("dataset/dataset.csv")

cv = CountVectorizer()
vectors = cv.fit_transform(df["tags"]).toarray()

similarity = cosine_similarity(vectors)

pickle.dump(df, open("models/df.pkl", "wb"))
pickle.dump(similarity, open("models/similarity.pkl", "wb"))

print("Model trained successfully")
