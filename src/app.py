from flask import Flask
from flask import request
from flask import jsonify
import datetime

import utils
import hit


startTime = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
killApp = False

app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
    global killApp

    if killApp:
        raise Exception("Sorry, this container is killed")
    
    return "hello"

@app.route("/kill")
def killapp():
    global killApp
    killApp = True
    return "Ok, setting app to be killed"

@app.route("/")
def show_details() :
    global startTime
    global killApp

    if killApp:
        raise Exception("Sorry, this container is killed")

    return "<html>" + \
           "<head><title>Docker + Flask Demo</title></head>" + \
           "<body>" + \
           "<table>" + \
           "<tr><td> Start Time </td> <td>" +  startTime + "</td> </tr>" \
           "<tr><td> Hostname </td> <td>" + utils.gethostname() + "</td> </tr>" \
           "<tr><td> Local Address </td> <td>" + utils.getlocaladdress() + "</td> </tr>" \
           "<tr><td> Remote Address </td> <td>" + request.remote_addr + "</td> </tr>" \
           "<tr><td> Server Hit </td> <td>" + str(hit.getServerHitCount()) + "</td> </tr>" \
           "</table>" + \
            "<hr/>" + \
            "<span><a href='/kill'>Kill this container</a></span>" + \
           "</body>" + \
           "</html>"

@app.route("/json")
def send_json() :
    global startTime
    return jsonify( {'StartTime' : startTime,
                     'Hostname': utils.gethostname(),
                     'LocalAddress': utils.getlocaladdress(),
                     'RemoteAddress':  request.remote_addr,
                     'Server Hit': str(hit.getServerHitCount())} )

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0')
