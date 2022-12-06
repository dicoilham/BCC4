from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

import pandas as pd
import re
from TPCCP4 import preprocess
import sqlite3

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API Deploymen Chalange 4'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API Chalange 4')
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'dokumentasi',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/dokumentasi/"
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)

@swag_from("template/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text_ = request.form.get('text')

    df = pd.DataFrame([{'text':text_}])
    print (df)

    df_clean ['clean']= df['text'].apply (lambda x: preprocess (x))
    print (df_clean)
    
    conn = sqlite3.connect('db_gold.db')
    cur = conn.cursor()
    print("Opened database successfully")

    rows = [(text_, df_clean['clean'][0])]
    cur.executemany(''' INSERT INTO data_clean (text_before, text_after) VALUES (?,?)''', rows)
    print ('data entered')

    conn.commit()
    if (conn):
        conn.close()
        print ('conn closed')


    json_response = {
        'status_code': 200,
        'data': df_clean['clean'][0]
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("template/text-file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    text_ = request.form.get('file') # nama file csv /path csv ex : 'data.csv'
    nama_kolom = request.form.get('nama_kolom')


    # df = pd.DataFrame([{'text':text_}])
    df = pd.read_csv(text_, encoding='iso-8859-1')
    print (df)

    # df_clean = prepros (df, nama_kolom)
    df_clean['clean'] = df[nama_kolom].apply(lambda x : reprocess (x))
    print (df_clean)

    sql_data = 'db_gold.db'
    conn = sq.connect(sql_data)
    cur = conn.cursor()

    df_clean.to_sql('data_clean', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

    json_response = {
        'status_code': 200,
        'data': list(df_clean['clean'])
    }
    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()


