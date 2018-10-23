import snowflake.connector
import os
from flask import Flask,request, Response,jsonify
#needed to get the environment variables
from dotenv import load_dotenv
from os.path import join, dirname
#needed to get the environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)


ctx = snowflake.connector.connect(
    user = os.environ.get('snowflake_username'),
    password=os.environ.get('snowflake_password'),
    account='petco.us-east-1'
        )
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
#ctx.close()

#test slack actually works
@app.route('/slack', methods=['GET'])
def slack():
    
    return jsonify({"Success" : True , "Payload" :  "testing"})

#test snowflake connecter
@app.route('/snowflake', methods=['GET'])
def snowflake():
    try:
        query = ctx.cursor()
        query.execute('SELECT SHIPMENT_KEY FROM "WHPRD_VW"."DWADMIN"."F_OMS_YFS_SHIPMENT" LIMIT 1')
        print(query)
        one_row = query.fetchmany(5)
        test = one_row[0]
        print(one_row[0])
    finally:
        query.close()

    return jsonify({"Success" : True , "Payload" :  test})

if __name__ == "__main__":
    #Running the flask app
    app.run() 