# Iris Classification system
import streamlit as st
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# page header
st.markdown("""
## Iris Flower Prediction App  

This will be used to predict iris flower type                       
""")

# create input parameters on the sidebar
st.sidebar.header('Sepal and Petal Parameters')

# create classification system
def input_features():
    sepal_length = st.sidebar.slider('Sepal Length (cm)', min_value=4.30, max_value=7.90, value=6.10)
    sepal_width = st.sidebar.slider('Sepal Width (cm)', min_value=2.00, max_value=4.40, value=3.20)
    petal_length = st.sidebar.slider('Petal Length (cm)', min_value=1.00, max_value=4.50, value=2.75)
    petal_width = st.sidebar.slider('Petal Width (cm)', min_value=0.10, max_value=2.50, value=1.20)
    
    input = {'sepal_length':sepal_length,
             'sepal_width': sepal_width,
             'petal_length': petal_length,
             'petal_width': petal_width}
    features = pd.DataFrame(input, index=[0])

    return features




## ------------------------------------------------------------------------------ ##
# creates the data frame on main page
df = input_features()
st.subheader('Flower Parameters')
# shows the df underneath our titles
st.write(df)


# load data and build classification model
iris = datasets.load_iris()
X=iris.data
Y=iris.target

# initiate the model
clf = RandomForestClassifier()
clf.fit(X, Y)

# predict using the input data
prediction = clf.predict(df)
prediction_proba = clf.predict_proba(df)

# flower types box
st.subheader('Class labels for flowers')
st.write(iris.target_names)

# prediction box
st.subheader('Prediction')
st.write(iris.target_names[prediction])

# prediction probability of each flower
st.subheader('Prediction Probability')
st.markdown("""
0: Setosa  
1: Versicolor  
2: Virginica              
""")
st.write(prediction_proba)






