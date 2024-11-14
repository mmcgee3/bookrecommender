import pandas as pd

# Load data
books_df = pd.read_csv('data/Books.csv')
ratings_df = pd.read_csv('data/Ratings.csv')
initial_book_count = len(books_df)
initial_review_count = len(ratings_df)

# Count reviews for each book
review_counts = ratings_df['ISBN'].value_counts()

# Filter books that meet the minimum review threshold
popular_books = review_counts[review_counts >= 40].index
filtered_books_df = books_df[books_df['ISBN'].isin(popular_books)]

# Filter ratings for the books that meet the threshold
filtered_ratings_df = ratings_df[ratings_df['ISBN'].isin(popular_books)]

# Save the filtered data
filtered_books_df.to_csv('data/BooksFiltered.csv', index=False)
filtered_ratings_df.to_csv('data/RatingsFiltered.csv', index=False)

print(f"Number of books remaing: {len(filtered_books_df)}")
print(f"Number of reviews remaing: {len(filtered_ratings_df)}")