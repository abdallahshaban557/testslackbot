from flask import Flask,request, Response,jsonify
app = Flask(__name__)


@app.route('/slack', methods=['GET'])
def CheckUnreadAlerts():
    return jsonify({"Success" : True , "Payload" :  "testing"})


if __name__ == "__main__":
    #Running the flask app
    app.run() 