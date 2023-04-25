# Importing libraries
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
import pickle

# Read the clean dataset
reviews = pd.read_csv('../data/clean_train.csv')

X = reviews['content_stem']
y = reviews['target']

# Perform train test split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print('Creating TFIDF Naive Bayes Model')
# Create a pipeline with TF-IDF and Naive Bayes
pipe_tvec_nb = Pipeline([
    ('tvec', TfidfVectorizer(stop_words='english')),
    ('nb', MultinomialNB())
])

# Search over the following values of hyperparameters:
pipe_tvec_nb_params = {
    'tvec__max_features': [500], #200
    'tvec__min_df': [2,3], #
    'tvec__max_df': [.9,.95], 
#     'tvec__ngram_range':[(1,1),(1,2)],  
}

# Instantiate GridSearchCV
gs_tvec_nb = GridSearchCV(pipe_tvec_nb, # Objects to optimise
                          param_grid = pipe_tvec_nb_params, # Hyperparameters for tuning
                          cv=10) # 10-fold cross validation

# Fit model on to training data
gs_tvec_nb.fit(X_train, y_train)


print('Saving model to disk')
# Saving model to disk
pickle.dump(gs_tvec_nb, open('modelNB.pkl','wb'))

# Loading model to compare the results
# model = pickle.load(open('model.pkl','rb'))
# print(model.predict([[2, 9, 6]]))
