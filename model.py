
#importing modules
import pandas as pd
import numpy as np
import re
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout, Activation
from keras.utils import to_categorical


#Global Functions for data cleaning
# Global Functions
def extract_hashtags(text):
    if isinstance(text, (str, bytes)):
        return re.findall(r'#\w+', text)
    else:
        return "NaN"
    
def clean_text(text):
    # remove URLs
    text = re.sub(r'https?:\/\/\S+', '', text)
    
    # remove hashtags and mentions
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'@\w+', '', text)
    
    # remove special characters and punctuation
    text = re.sub(r'[@$!#%&()*+,-./:;<=>?[\]^_`{|}~]', '', text)
    
    # remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # remove emojis
    text = text.encode('ascii', 'ignore').decode()
    return text


dataset = pd.read_csv("final_merged.csv")
dataset.head(30)

#Data Preprocessing
# remove all rows with empty post captions
dataset = dataset.dropna(subset=['Post Captions'])

#add all hashtags to another column 
dataset['extracted hashtags'] = dataset['Post Captions'].apply(extract_hashtags)

#remove all hashtags and mentions from post captions and urls
dataset['cleaned text'] = dataset['Post Captions'].apply(clean_text)

#load data out to tag it manually
# dataset.to_csv('cleaned_data2.csv', index=False)


# perform feature engineering to convert text data into numerical features
#performing bag of words
tagged_df = pd.read_csv("final_merged_tagged.csv")

tagged_df = tagged_df.filter(regex='^(?!Unnamed)')

tagged_df = tagged_df.dropna(subset=['cleaned text'])

tagged_df = tagged_df.dropna(subset=['TAG'])

tagged_df.head(30)


# define the input and output columns
X = tagged_df['cleaned text']
y = tagged_df['TAG']
# print(X)

#splitting our dataset
train_posts, test_posts, train_tags, test_tags = train_test_split(X, y, test_size=0.2, random_state=42)
# print(train_posts)
# print(train_tags)
# print(test_posts)
# print(test_tags)

#convert labels to binary vectors
vocab_size = 1000
tokenize = Tokenizer(num_words=vocab_size, char_level=False)
tokenize.fit_on_texts(train_posts)

#creating training data
X_train = tokenize.texts_to_matrix(train_posts)
X_test = tokenize.texts_to_matrix(test_posts)


#creating testing data
encoder = LabelEncoder()
encoder.fit(train_tags)
y_train = encoder.transform(train_tags)
y_test = encoder.transform(test_tags)

num_classes = np.max(y_train) + 1
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

# Inspect the dimenstions of our training and test data (this is helpful to debug)
# print('x_train shape:', X_train.shape, X_train.dtype)
# print('x_test shape:', X_test.shape, X_test.dtype)
# print('y_train shape:', y_train.shape, y_train.dtype)
# print('y_test shape:', y_test.shape,y_test.dtype)
# print('number of classes:', num_classes)	

class Model():
    def __init__(self, batch_size, epochs):
        self.batch_size = batch_size
        self.epochs = epochs
    
    def model(self):
        # Build the model
        model = Sequential()
        model.add(Dense(512, input_shape=(vocab_size,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['accuracy'])
        return model

    def fit_model(self, model):
        history = model.fit(X_train, y_train, batch_size=self.batch_size, epochs=self.epochs, verbose=1, validation_split=0.1)
        return history
    
    def score_model(self, model):
        score = model.evaluate(X_test, y_test, batch_size=self.batch_size, verbose=1)
        return score
    
    def generate_predictions(self, model, x_test):
        text_labels = encoder.classes_
        predictions = []
        for i in range(len(x_test)):
            prediction = model.predict(np.array([x_test[i]]))
            predicted_label = text_labels[np.argmax(prediction)]
            actual_label = test_tags.iloc[i]
            post = test_posts.iloc[i][:50]
            result = {"post": post, "actual_label": actual_label, "predicted_label": predicted_label}
            predictions.append(result)
        return json.dumps(predictions)


def start_model():
    model_obj = Model(batch_size=10, epochs=5)
    model = model_obj.model()
    print(model.summary())

    model_obj.fit_model(model)
    score = model_obj.score_model(model)

    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    results = model_obj.generate_predictions(model, X_test)
    return results


