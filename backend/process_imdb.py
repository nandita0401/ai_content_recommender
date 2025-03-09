import pandas as pd
from pymongo import MongoClient

# ✅ Load IMDb datasets
print("📥 Loading IMDb Data...")
movies_df = pd.read_csv("backend/title.basics.tsv", sep="\t", low_memory=False, encoding="utf-8")
ratings_df = pd.read_csv("backend/title.ratings.tsv", sep="\t", low_memory=False, encoding="utf-8")

# ✅ Filter only 'movie' type (Remove TV Shows, Shorts, etc.)
movies_df = movies_df[movies_df["titleType"] == "movie"]

# ✅ Merge ratings with movie details
movies_df = movies_df.merge(ratings_df, on="tconst", how="left")

# ✅ Keep only necessary columns
movies_df = movies_df[["tconst", "primaryTitle", "genres", "startYear", "averageRating"]]

# ✅ Rename columns for readability
movies_df.rename(columns={
    "tconst": "imdb_id",
    "primaryTitle": "title",
    "genres": "genre",
    "startYear": "year",
    "averageRating": "rating"
}, inplace=True)

# ✅ Convert NaN ratings to 0
movies_df["rating"] = movies_df["rating"].fillna(0)

movies_df["genres"] = movies_df["genres"].replace("\\N", "Unknown")


# ✅ Convert year to integer (remove \N values)
movies_df = movies_df[movies_df["year"] != "\\N"]
movies_df["year"] = movies_df["year"].astype(int)

# ✅ Filter movies released in 2000 and later (Optional)
movies_df = movies_df[movies_df["year"] >= 2000]

# ✅ Save cleaned data to CSV
movies_df.to_csv("backend/cleaned_imdb_movies.csv", index=False)
print("✅ IMDb Data Processed & Saved as 'backend/cleaned_imdb_movies.csv'")

# ✅ Connect to MongoDB and Insert Data
client = MongoClient("mongodb://localhost:27017/")
db = client["imdb_database"]
movies_collection = db["movies"]

# ✅ Insert Only if Collection is Empty
if movies_collection.count_documents({}) == 0:
    movies_collection.insert_many(movies_df.to_dict(orient="records"))
    print("✅ IMDb Movies inserted into MongoDB!")
else:
    print("✅ IMDb Movies already exist in MongoDB!")
