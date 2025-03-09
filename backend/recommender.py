import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

# Load movie ratings dataset
df = pd.read_csv("ratings.csv")  # Use a dataset like MovieLens
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.2)
model = SVD()
model.fit(trainset)

def recommend_movie(user_id, movie_id):
    return model.predict(user_id, movie_id).est
