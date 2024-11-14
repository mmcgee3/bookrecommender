import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

# Load the user-item matrix with USER-ID as the index and transpose it
user_item_matrix = pd.read_csv("data/UserItem.csv", index_col="User-ID").T

# Load the book names with their ISBNs from the books CSV
book_names = pd.read_csv("data/BooksFiltered.csv", low_memory=False)  # Ensure 'ISBN' and 'Book-Title' are columns in this file

# Define and fit the KNN model on the transposed user-item matrix
cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
cf_knn_model.fit(user_item_matrix)

def book_recommender_engine(book_title, matrix, cf_model, n_recs):
    # Find the closest match ISBN for the input book title
    matched_title = process.extractOne(book_title, book_names['Book-Title'])
    if matched_title:
        book_id = book_names[book_names['Book-Title'] == matched_title[0]]['ISBN'].values[0]

        # Check if the ISBN exists in the transposed user-item matrix rows (formerly columns)
        if book_id in matrix.index:
            # Calculate neighbor distances
            distances, indices = cf_model.kneighbors(matrix.loc[book_id].values.reshape(1, -1), n_neighbors=n_recs)
            book_rec_ids = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[1:]
            
            cf_recs = []
            for i in book_rec_ids:
                isbn = matrix.index[i[0]] 
                title = book_names.loc[book_names['ISBN'] == isbn, 'Book-Title'].values[0]
                cf_recs.append({'Title': title, 'Distance': i[1]})

            # Select the top recommendations
            df = pd.DataFrame(cf_recs, index=range(1, n_recs))

            return df
        else:
            print(f"ISBN {book_id} not found in user-item matrix.")
    else:
        print("Book title not found in the dataset.")

    return pd.DataFrame()

n_recs = 10
user_book = input("Enter a book title: ")
print(book_recommender_engine(user_book, user_item_matrix, cf_knn_model, n_recs))
