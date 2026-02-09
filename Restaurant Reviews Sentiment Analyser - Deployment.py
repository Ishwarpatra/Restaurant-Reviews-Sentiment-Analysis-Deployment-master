# Importing essential libraries
import pandas as pd
import pickle

# Loading the dataset
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, 'Restaurant_Reviews.tsv')
df = pd.read_csv(dataset_path, delimiter='\t', quoting=3)

# Importing essential libraries for performing Natural Language Processing on 'Restaurant_Reviews.tsv' dataset
import nltk
import re
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Cleaning the reviews
corpus = []
for i in range(0,1000):

  # Cleaning special character from the reviews
  review = re.sub(pattern='[^a-zA-Z]',repl=' ', string=df['Review'][i])

  # Converting the entire review into lower case
  review = review.lower()

  # Tokenizing the review by words
  review_words = review.split()

  # Removing the stop words
  review_words = [word for word in review_words if not word in set(stopwords.words('english'))]

  # Lemmatizing the words
  lemmatizer = WordNetLemmatizer()
  review = [lemmatizer.lemmatize(word) for word in review_words]

  # Joining the lemmatized words
  review = ' '.join(review)

  # Creating a corpus
  corpus.append(review)

# Creating the TF-IDF model (replacing Bag of Words)
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()  # Removed max_features constraint
X = tfidf.fit_transform(corpus).toarray()
y = df.iloc[:, 1].values

# Creating a pickle file for the TfidfVectorizer
pickle.dump(tfidf, open('cv-transform.pkl', 'wb'))


# Model Building

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import MultinomialNB
classifier = MultinomialNB(alpha=0.2)
classifier.fit(X_train, y_train)

# Creating a pickle file for the Multinomial Naive Bayes model
filename = 'restaurant-sentiment-mnb-model.pkl'
pickle.dump(classifier, open(filename, 'wb'))

# Model Evaluation Metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
y_pred = classifier.predict(X_test)
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")