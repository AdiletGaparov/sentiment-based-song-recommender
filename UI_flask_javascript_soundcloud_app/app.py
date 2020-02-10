from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    subject = None
    level = None
    selected_choice = ""
    songs = []

    lyrics = pd.read_csv('lyrics_sentiment.csv')

    subjectivity_dict = {'subjective-20': 'Python, R, SQL',
                          'subjective-40': 'Hadoop, Spark, Streaming',
                          'subjective-60': 'Machine Learning',
                          'subjective-80': 'Data Visualization',
                          'subjective-100': 'Ethics, Agile, Design Thinking'}

    polarity_dict = {'very-low': 'I am ready!',
                     'low': 'Need to recap few concepts',
                     'average': 'I still have few more days',
                     'high': 'Proficiency is a good grade',
                     'very-high': 'God bless Gaussian curve at IE'}

    if request.method == "POST":
        subject = request.form.get('subject-choice')
        level = request.form.get('despair-level')
        genre = request.form.get('genre')
        selected_choice = f'{subjectivity_dict.get(subject)} / {polarity_dict.get(level)} / {genre}'

        subj_genre_filter = get_filter(lyrics, subject, genre)
        polarity_scores = lyrics.loc[subj_genre_filter, 'polarity_avg'].unique()

        t_min, t_max = get_polarity_threshold(polarity_scores, level)

        lyrics_filtered = lyrics.loc[subj_genre_filter & (lyrics['polarity_avg'] <= t_max) & (lyrics['polarity_avg'] >= t_min)].sort_values('polarity_avg')

        song_names = lyrics_filtered.song
        artist_names = lyrics_filtered.artist

        songs = [song + " by " + artist for song, artist in zip(song_names, artist_names)]

    return render_template('index.html', songs=songs[:20], selected_choice=selected_choice)

def get_polarity_threshold(polarity_scores, level):
    """Get threshold for polarities based on percentile"""
    
    if level == 'very-low':
        t_max = np.percentile(polarity_scores, 20)
        t_min = np.percentile(polarity_scores, 0)
    elif level == 'low':
        t_max = np.percentile(polarity_scores, 40)
        t_min = np.percentile(polarity_scores, 20)
    elif level == 'average':
        t_max = np.percentile(polarity_scores, 60)
        t_min = np.percentile(polarity_scores, 40)
    elif level == 'high':
        t_max = np.percentile(polarity_scores, 80)
        t_min = np.percentile(polarity_scores, 60)
    elif level == 'very-high':
        t_max = np.percentile(polarity_scores, 100)
        t_min = np.percentile(polarity_scores, 80)
    else:
        t_max = np.percentile(polarity_scores, 100)
        t_min = np.percentile(polarity_scores, 0)

    return t_min, t_max

def get_filter(df, subject, genre):
    """Get boolean array that filters based on subjectivity and genre level"""
    
    if genre == '':
        genre_list = df.genre.unique()
    else:
        genre_list = [genre]

    if subject == 'subjective-20':
        filter_array = (df['subjectivity_avg'] <= 0.2) & (df['genre'].isin(genre_list))
    elif subject == 'subjective-40':
        filter_array = (df['subjectivity_avg'] > 0.2) & (df['subjectivity_avg'] <= 0.4) & (df['genre'].isin(genre_list))
    elif subject == 'subjective-60':
        filter_array = (df['subjectivity_avg'] > 0.4) & (df['subjectivity_avg'] <= 0.6) & (df['genre'].isin(genre_list))
    elif subject == 'subjective-80':
        filter_array = (df['subjectivity_avg'] > 0.6) & (df['subjectivity_avg'] <= 0.8) & (df['genre'].isin(genre_list))
    elif subject == 'subjective-100':
        filter_array = (df['subjectivity_avg'] > 0.6) & (df['subjectivity_avg'] <= 0.8) & (df['genre'].isin(genre_list))
    else:
        filter_array = df['genre'].isin(genre_list)

    return filter_array

if __name__ == '__main__':
    app.run()
