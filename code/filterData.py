import pandas as pd

# Load data
books_df = pd.read_csv('data/Books.csv')
ratings_df = pd.read_csv('data/Ratings.csv')
initial_book_count = len(books_df)
initial_review_count = len(ratings_df)

# Merge duplicates by ISBN and Title, keeping first non-null entries for other columns
books_df = books_df.groupby(['ISBN', 'Book-Title'], as_index=False).first()

# Count reviews for each book
review_counts = ratings_df['ISBN'].value_counts()

# Filter books that meet the minimum review threshold
popular_books = review_counts[review_counts >= 20].index
filtered_books_df = books_df[books_df['ISBN'].isin(popular_books)]

# Filter ratings for the books that meet the threshold
filtered_ratings_df = ratings_df[ratings_df['ISBN'].isin(popular_books)]

# Save the filtered data
filtered_books_df.to_csv('data/BooksFiltered.csv', index=False)
filtered_ratings_df.to_csv('data/RatingsFiltered.csv', index=False)

print(f"Initial number of books: {initial_book_count}")
print(f"Initial number of reviews: {initial_review_count}")
print(f"Number of books remaining after merge and filtering: {len(filtered_books_df)}")
print(f"Number of reviews remaining: {len(filtered_ratings_df)}")
