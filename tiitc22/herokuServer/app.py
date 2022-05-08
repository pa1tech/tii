from flask import Flask, flash,render_template, request, send_from_directory,session
import time,os

app = Flask(__name__)
app.secret_key = 'the random string'
  
# Define TZ environment variable
os.environ['TZ'] = 'Asia/Kolkata'
# reset the time conversion rules
time.tzset()

'''f = open("gg.txt", "w")
f.write('00'); f.close()'''

lastPing = time.strftime('%d %b - %H:%M:%S', time.localtime())

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        status =  ['0','0']
        if request.form.get('rc') == 'on':
            status[0] = '1'
        else:
            status[0] = '0'
        if request.form.get('wh') == 'on':
            status[1] = '1'
        else:
            status[1] = '0'
        msg = ''.join(status)

        f = open("gg.txt", "w")
        f.write(msg); f.close()

        print(msg)
        return render_template('index.html',statusMsg=msg,lastPing=lastPing)
    else:
        f = open("gg.txt", "r")
        msg = f.read(); f.close()
        print(msg)
        return render_template('index.html',statusMsg=msg,lastPing=lastPing)

@app.route('/esp',methods=['GET'])
def index1():
    if request.method == 'GET':
        global lastPing
        f = open("gg.txt", "r")
        msg = f.read(); f.close()
        lastPing = time.strftime('%d %b - %H:%M:%S', time.localtime())
        print(msg)
        return (msg)
 
'''@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')'''
  
    
    
if __name__ == "__main__":
        app.run()
