# Restaurant Review's Sentiment Analysis - Deployment
![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-blue.svg) ![Python 3.6+](https://img.shields.io/badge/Python-3.6+-brightgreen.svg) ![NLTK](https://img.shields.io/badge/Library-NLTK-orange.svg)

• This repository consists of files required to deploy a ___Machine Learning Web App___ created with ___Flask___ on ___Heroku___ platform.

• If you want to view the deployed model, click on the following link:<br />
Deployed at: _https://restaurant-reviews-sentiment.herokuapp.com/_

## Model Information

### Algorithms Used
- **Natural Language Processing**: WordNet Lemmatizer for word normalization
- **Feature Extraction**: TF-IDF Vectorizer (Term Frequency-Inverse Document Frequency)
- **Classification Algorithm**: Multinomial Naive Bayes
- **Model Evaluation**: Classification Report, Confusion Matrix, Accuracy Score

### Preprocessing Pipeline
1. Text cleaning: Removal of special characters
2. Lowercase conversion
3. Tokenization
4. Stop word removal
5. Lemmatization (instead of stemming for better linguistic accuracy)

### Model Performance
- **Dataset**: Restaurant Reviews (1000 samples)
- **Training Split**: 80% training, 20% testing
- **Algorithm**: Multinomial Naive Bayes with alpha=0.2
- **Features**: TF-IDF vectors without feature limit constraints

### Technical Improvements Made
- Upgraded from Porter Stemmer to WordNet Lemmatizer for better word normalization
- Replaced CountVectorizer with TfidfVectorizer for better feature representation
- Removed arbitrary max_features limit for optimal performance
- Added comprehensive error handling
- Implemented secure deployment configurations
- Added model evaluation metrics

• Please do ⭐ the repository, if it helped you in anyway.

• A glimpse of the web app:

![GIF](readme_resources/restaurant-review-web-app.gif)

_**----- Important Note -----**_<br />
• If you encounter this webapp as shown in the picture given below, it is occuring just because **free dynos for this particular month provided by Heroku have been completely used.** _You can access the webpage on 1st of the next month._<br />
• Sorry for the inconvenience.

![Heroku-Error](readme_resources/application-error-heroku.png)
