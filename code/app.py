# app.py
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

app = Flask(__name__)

# Load the datasets and fit the model
user_item_matrix = pd.read_csv("data/UserItem.csv", index_col="User-ID").T
book_names = pd.read_csv("data/BooksFiltered.csv", low_memory=False)
cf_knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
cf_knn_model.fit(user_item_matrix)

def book_recommender_engine(book_title, matrix, cf_model, n_recs=6):
    matched_title = process.extractOne(book_title, book_names['Book-Title'])
    if matched_title:
        book_id = book_names[book_names['Book-Title'] == matched_title[0]]['ISBN'].values[0]
        if book_id in matrix.index:
            distances, indices = cf_model.kneighbors(matrix.loc[book_id].values.reshape(1, -1), n_neighbors=n_recs)
            book_rec_ids = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[1:]
            
            cf_recs = [{
                'Title': book_names.loc[book_names['ISBN'] == matrix.index[i[0]], 'Book-Title'].values[0],
                'ISBN': matrix.index[i[0]],
                'Image-URL-M': book_names.loc[book_names['ISBN'] == matrix.index[i[0]], 'Image-URL-M'].values[0],  # Include image URL
                'Distance': i[1]
            } for i in book_rec_ids]
            return cf_recs
    return []

@app.route('/', methods=['GET'])
def index():
    books_list = book_names[['Book-Title', 'ISBN', 'Image-URL-M']].to_dict(orient='records')  # Include Image-URL-M
    return render_template('index.html', books=books_list)


@app.route('/get_book_info', methods=['GET'])
def get_book_info():
    isbn_or_title = request.args.get('isbnOrTitle', '').strip()
    if isbn_or_title.isdigit():
        book = book_names[book_names['ISBN'] == isbn_or_title]
    else:
        book = book_names[book_names['Book-Title'].str.contains(isbn_or_title, case=False)]
    if not book.empty:
        return jsonify({'isbn': book['ISBN'].values[0], 'title': book['Book-Title'].values[0]})
    return jsonify({'isbn': '', 'title': ''})

@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form.get('book_title')
    recommendations = book_recommender_engine(book_title, user_item_matrix, cf_knn_model)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
