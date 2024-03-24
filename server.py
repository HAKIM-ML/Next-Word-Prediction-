import os
import pickle

import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Define local file paths for model, tokenizer, and max sequence length
model_cache_path = "F:\\class\\DeepLearning\\Nlp Project\\Next word prediction\\Next Word Predictor\\text_predictor.h5"
tokenizer_cache_path = "F:\\class\\DeepLearning\\Nlp Project\\Next word prediction\\Next Word Predictor\\tokenizer.pkl"
max_seq_length_cache_path = "F:\\class\\DeepLearning\\Nlp Project\\Next word prediction\\Next Word Predictor\\max_sequence_length"

# Load the model, tokenizer, and max sequence length
model = load_model(model_cache_path)
with open(tokenizer_cache_path, 'rb') as file:
    tokenizer = pickle.load(file)
with open(max_seq_length_cache_path, 'rb') as file:
    max_sequence_len = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html')


def generate_recommendations_from_model(seed_text, next_words=3):
    recommendations = []
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted_probabilities = model.predict(token_list, verbose=0)
        predicted_index = np.argmax(predicted_probabilities)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break
        seed_text += " " + output_word
        recommendations.append(seed_text)
    return recommendations


@app.route('/predict', methods=['POST'])
def predict():
    seed_text = request.form['seed_text']
    next_words = 3  # You can adjust this value based on how many words you want to predict
    recommendations = generate_recommendations_from_model(seed_text, next_words)
    return {'recommendations': recommendations}


if __name__ == '__main__':
    app.run(debug=True)
