import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

user_ratings_df = pd.read_csv("data/RatingsFiltered.csv")

user_item_matrix = user_ratings_df.pivot(index=['User-ID'], columns=['ISBN'], values='Book-Rating').fillna(0)

user_item_matrix.to_csv('data/UserItem.csv', index=True)