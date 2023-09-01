from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime
import gspread
import pickle
import numpy as np
from flask_mail import Mail, Message
from threading import Lock


gc = gspread.service_account('/home/smartsocket/mysite/smart-socket-374918-c98ad65883f5.json')
gc_1 = gspread.service_account('/home/smartsocket/mysite/smart-socket-database-2-e511b5d3326a.json')
sh = gc.open("Smart socket database( every 10 minutes)")
sh_1 = gc_1.open("Smart socket database")
wks = sh.worksheet("Sheet1")
wks_1 = sh_1.worksheet("Sheet1")

last_value = wks.get_all_values()[-1][2:]
last_value_1 = wks_1.get_all_values()[-1][2:]

last_value_float = [float(i) for i in last_value]
last_value_1_float = [float(i) for i in last_value_1]

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smartsocket@401'
socketio = SocketIO(app, cors_allowed_origins='*')
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'smartsocketeee401@gmail.com'
app.config['MAIL_PASSWORD'] = 'satuyedmerqgzlzx'
app.config['MAIL_DEFAULT_SENDER'] = ('Smart socket')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False


def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

with open('/home/smartsocket/mysite/model_Isolation_forest_0.pkl', 'rb') as a:
    model_0 = pickle.load(a)

with open('/home/smartsocket/mysite/model_Isolation_forest_1.pkl', 'rb') as b:
    model_1 = pickle.load(b)
alert = False

def get_updated_data(updated_data):
    global last_value_float
    if last_value_float != updated_data:
        last_value_float = updated_data
        return last_value_float
    return None


def get_updated_data_1(updated_data_1):
    global last_value_1_float
    if last_value_1_float != updated_data_1:
        last_value_1_float = updated_data_1
        return last_value_1_float
    return None

@app.route('/')
def index():

    return render_template('index.html')

def background_thread():
    print("Generating random sensor values")
    with app.app_context():
        while True:
            socketio.sleep(1)

            updated_data_1 = get_updated_data_1(list(float(i) for i in wks_1.get_all_values()[-1][2:]))

            if updated_data_1 is not None:
                socketio.emit('updateSensorData', {'value': updated_data_1[0],'valuea': updated_data_1[1],'valueb': updated_data_1[2],'valuec': updated_data_1[3],'valued': updated_data_1[4],  "date": get_current_datetime()})

                selected_elements_1 = updated_data_1[3]
                input_data_to_numpy_array_1 = np.asarray(selected_elements_1)
                input_data_reshaped_1 = input_data_to_numpy_array_1.reshape(1, -1)
                u = input_data_reshaped_1
                x_1 = model_1.predict(u)
                if x_1 == -1:
                    mail = Mail(app)
                    msg = Message('Anomalous consumption of Power detected', recipients=['ogundejiabiola96@gmail.com'])
                    msg.html = '<b> There is an anomalous consumption of power<b> '
                    if updated_data_1 is not None:
                        msg.html += f"<p>Updated data: {updated_data_1}</p>"
                    mail.send(msg)

            updated_data = get_updated_data(list(float(i) for i in wks.get_all_values()[-1][2:]))
            if updated_data is not None:
                selected_elements = updated_data[4]
                input_data_to_numpy_array = np.asarray(selected_elements)
                input_data_reshaped = input_data_to_numpy_array.reshape(1, -1)
                v = input_data_reshaped
                x_0 = model_0.predict(v)
                if x_0 == -1:
                    mail = Mail(app)
                    msg = Message('Anomalous consumption of energy detected', recipients=['ogundejiabiola96@gmail.com'])
                    msg.html = '<b> There is an anomalous consumption of energy <b> <p> check for the following : <p\> <p>Ensure there are no air leaks around windows, doors, or vents. This could increase the area of cooling and make your AC work harder to maintain the set temperature.</p><p>Adjust your thermostat to avoid overworking your AC</p><p>check for heat sources in your home,to reduce the workload on your AC.</p>'
                    if updated_data is not None:
                        msg.html += f"<p>Updated data: {updated_data}</p>"
                    mail.send(msg)


@socketio.on('connect')
def connect():

    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)






