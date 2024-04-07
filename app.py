from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load pickled data
new = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation', methods=['POST'])
def recommendation():
    if request.method == 'POST':
        # Get movie name from form
        movie_name = request.form['movie_name']
        recommended_movies = [] 
        
        # Check if the movie exists in the dataset
        if movie_name not in new['title'].values:
            return render_template('recommendation.html', movie_name=movie_name, recommendations_list=[])
        
        index = new[new['title'] == movie_name].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        # Get top 5 similar movies
        for i in distances[1:6]:
            recommended_movies.append(new.iloc[i[0]].title) 
        
        return render_template('recommendation.html', movie_name=movie_name, recommendations_list=recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)
