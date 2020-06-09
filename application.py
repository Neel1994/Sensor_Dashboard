#!/usr/bin/env python
# coding: utf-8

# In[65]:


import pandas as pd
from flask import Flask, jsonify, Response
import os
from flask_cors import CORS, cross_origin


# In[66]:


def data_processing(dataframe,index):
    if dataframe['server'].unique()[0] == '100.101.2.50':
       df = dataframe.drop(['Unnamed: 0','model_name','proc_core_speed','proc_l2_cache','proc_l3_cache',"CPU1VCoreVR",'CPU2VCoreVR','CPU1MEM0123VR','CPU1MEM4567VR','CPU2MEM0123VR','CPU2MEM4567VR'],axis=1) 
       df = df.dropna() 
        
    elif dataframe['server'].unique()[0] == '100.101.2.69':
        columns = [x+"A" if not(x.endswith(("A","B","C","D","E","F"))) and x.startswith('Fan') else x for x in dataframe.columns]
        dataframe.columns = columns
        df = dataframe.dropna()
        df = df.drop(['Unnamed: 0','model_name','proc_core_speed','proc_l2_cache','proc_l3_cache'],axis=1)
        
    elif dataframe['server'].unique()[0] == '100.101.12.68':
        columns = [x+"A" if not(x.endswith(("A","B","C","D","E","F"))) and x.startswith('Fan') else x for x in dataframe.columns]
        dataframe.columns = columns
        df = dataframe.dropna()
        df = df.drop(['Unnamed: 0','model_name','proc_core_speed','proc_l2_cache','proc_l3_cache'],axis=1)
    
    
    else:
        df = dataframe.dropna()
        df = df.drop(['Unnamed: 0','model_name','proc_core_speed','proc_l2_cache','proc_l3_cache'],axis=1)
    return df


# In[67]:


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

path = 'DataSensNew'

@app.route('/get_data/<int:key>',methods=['GET'])
@cross_origin()
def get_data(key):
    for index, files in enumerate(os.listdir(path),1):
        if key == index:
            df = pd.read_csv(path+"/"+files)
            df = data_processing(df,index)
            json_data = df.to_json()
            return Response(json_data,mimetype='application/json')
        
    return jsonify({"Error":"Invalid Server Entered!! Please Enter a value between 1 to 8 i.e. the server number"})

@app.route('/')
def hello():
    return "Hello World!"

# In[68]:


if __name__ == '__main__':
    app.run(debug=False)


# In[ ]:




