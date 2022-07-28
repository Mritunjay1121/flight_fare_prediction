from flask import Flask
from housing.logger import logging
import sys
from housing.exception import FlightfareException
app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception("We are testing exception")
    except Exception as e:
        housing=FlightfareException(e,sys)
        logging.info(housing.error_message)
        logging.info("We are testing logging")
    return "Teri maa ki chut"


if __name__=="__main__":
    app.run(debug=True)
    