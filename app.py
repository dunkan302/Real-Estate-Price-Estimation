import pip
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

install('numpy')
install('pandas')
install('flask')
install('sklearn')

#import libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from flask import Flask, request, render_template


#Initialize the flask App
app = Flask(__name__)
df = pd.read_csv("BangaloreHousing.csv")
X = df.drop(['price'],axis=1)
y = df['price']
locations = list(X.columns[4:len(X.columns)-3])
model = LinearRegression()
model.fit(X,y)

def HouseQuery(avl,size,sqft,bath,loc,area):
    l = list(X.columns)
    loc_index = l.index(loc)
    at_index = l.index(area)
    x=[0]*X.shape[1]
    x[0] = avl
    x[1] = size
    x[2] = sqft
    x[3] = bath
    x[loc_index] = 1
    x[at_index] = 1 
    return x

#default page of our web-app
@app.route('/')
def home():
    return render_template('index.html',locations=locations)

#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():

    '''
    For rendering results on HTML GUI
    '''
    int_features = [i for i in request.form.values()]
    final_features = HouseQuery(int(int_features[1]),int(int_features[3]),float(int_features[5]),int(int_features[4]),(int_features[0]),(int_features[2]))
    prediction = model.predict(np.array(final_features).reshape(1,-1))

    output = round(prediction[0], 2)

    return render_template('index.html',locations=locations, prediction_text='The esimated cost is :{} Lakhs'.format(output))

if __name__ == "__main__":
    
    app.run(debug=True)