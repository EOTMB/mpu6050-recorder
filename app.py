from flask import *
import os
import signal

app = Flask(__name__)


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
    
    return render_template('trigger2.html')
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
