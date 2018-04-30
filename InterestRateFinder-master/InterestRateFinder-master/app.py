import os
import io
import pandas as pd
import numpy as np
from PIL import Image
import base64

import tensorflow as tf

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras import backend as K

from flask import Flask, request, redirect, jsonify, render_template
#import deeplearning modules
from keras.utils import to_categorical


import pandas as pd
import numpy as np
#import sklearn
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

app = Flask(__name__)
model = None
graph = None

def load_model_1():
    global model
    global graph
    model = load_model("loan_model_trained.h5")
    graph = K.get_session().graph



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #data = {"success": False}
    if request.method == 'POST':
        # read the base64 encoded string
        #image_string = request.form.get('digit')
        Int_Rate=10.00
        Investment = request.form.get('investment')
        Term = request.form.get('term')
        Grade = request.form.get('grade')
        Employment_Len = request.form.get('employment_length')
        Home_ownership = request.form.get('home_ownership')
        Annual_Income=request.form.get('annual_income')
        Purpose = request.form.get('purpose')
        State = request.form.get('state')
        Debt_To_Income = request.form.get('dti')
        Delinquence_2year = request.form.get('delinquency')
#            Int_Rate=5.32
#            Investment = 4800.0
#            Term = 36
#            Grade = "A"
#            Employment_Len = "2 years"
#            Home_Ownership = "MORTGAGE"
#            Annual_Income=143000.0
#            Purpose = "medical"
#            State = "KY"
#            Debt_To_Income = 7.88
#            Delinquence_2year = 0
            
        loan_array = [Int_Rate,Investment,Term,Grade,Employment_Len,Home_ownership,Annual_Income,Purpose,State,Debt_To_Income,Delinquence_2year]
        print(loan_array)
#
        user_input = pd.DataFrame(data=[loan_array],columns=['Int_Rate','Investment', 'Term', 'Grade', 'Employment_Len','Home_Ownership', 'Annual_Income', 'Purpose', 'State', 'Debt_To_Income','Delinquance_2year'])
        print(user_input)

        #load in our model
        model = keras.models.load_model("loan_model_trained.h5")
        #construct loan_input
        test_loan = pd.read_csv("Loan_Data3.csv")
#
#
        test_loan=test_loan.append(user_input)

        #encode the user input row along with the entire loan.csv

        for column in test_loan.columns:

            if test_loan[column].dtype == type(object):
                le = LabelEncoder()
                test_loan[column]=le.fit_transform(test_loan[column].astype(str))
            print(test_loan[column].dtype)    
        X=test_loan.drop("Int_Rate",axis=1)
        y=test_loan["Int_Rate"]
#
        #take one-hot-encoded last row to grab user input
        one_hot_input = test_loan.tail(1)
        print(one_hot_input)
        
#
        #drop the temporary Int_Rate from one_hot_input
        one_hot_input = one_hot_input.drop("Int_Rate",axis=1)

        #drop tail from dataset to ensure we have it in the train(will put it right back in)
        test_loan = test_loan.drop(test_loan.index[len(test_loan)-1])
        
        #split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.9, test_size=.1, random_state=1)
        
        #add one hot encoded user input row back to X_train
        X_train=X_train.append(one_hot_input)
##
        #finish fitting and transforming data
        X_scaler = StandardScaler().fit(X_train)

        X_train_scaled = X_scaler.transform(X_train)
        X_test_scaled = X_scaler.transform(X_test)

        label_encoder = LabelEncoder()
        label_encoder.fit(y_train)
#
        encoded_y_train = label_encoder.transform(y_train)
        encoded_y_test = label_encoder.transform(y_test)


        # Step 2: Convert encoded labels to one-hot-encoding
        y_train_categorical = to_categorical(encoded_y_train)
        y_test_categorical = to_categorical(encoded_y_test)
#
#
        #FINAL PREDICTION TIME!!!!!!


        encoded_predictions = model.predict_classes(X_train_scaled)

        prediction_labels = label_encoder.inverse_transform(encoded_predictions)

#        print(prediction_labels[-1])
        predicted_int_rate =prediction_labels[-1]
        print(predicted_int_rate)

        # indicate that the request was a success
        #data["prediction"] = predicted_int_rate
        #data["success"] = True
        result=predicted_int_rate
        print(result)



        return jsonify(result)
    return render_template("index.html")


if __name__ == "__main__":
    load_model_1()
    app.run()

