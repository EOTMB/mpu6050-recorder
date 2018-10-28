from flask import *
import io
import csv
import os
import signal
import numpy as np


app = Flask(__name__, static_url_path='')

medicion_path="medicion.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigger1')
def process1():
    #read process id from text file
    fh=open("processid.txt","r")
    processId = int(fh.read())
    fh.close()

    #send signal to process id
    os.kill(processId, signal.SIGUSR1)

    return render_template('trigger1.html')


@app.route('/trigger2')
def process2():
    #read process id from text file
    fh=open("processid.txt","r")
    processId = int(fh.read())
    fh.close()

    #send signal to process id
    os.kill(processId, signal.SIGUSR2)

    data = open(medicion_path,"r")
    #csvRead = csv.reader(data.read())
    #si = io.ByteIO()
    #cw = csv.writer(si)
    #cw.writerows(data.read())
    #output = make_response(si.getvalue())
    output = make_response(data.read())
    data.close()
    output.headers["Content-Disposition"] = "attachment; filename=medicion.csv"
    output.headers["Content-type"] = "text/csv"
    return output


    #return render_template('trigger2.html')
@app.route('/measure/<path:path>')
def send_measure(path):
    return send_from_directory('measure', path)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
