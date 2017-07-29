from functools import wraps
from flask import request, Response, Flask
import paho.mqtt.client as mqtt_client
import ConfigParser, os.path, sys

config_file = "/config/config.ini"

class MQTT_Helper():
    def __init__(self, client_id='', host='', port=1883, username='', password='', keepalive=30):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.keepalive = keepalive
        self.active = False
        self.connected = False

        """ Init the client """
        self.client = mqtt_client.Client(self.client_id)
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        if(self.username != '' and self.password != ''):
            self.client.username_pw_set(self.username, self.password)

    def exception_handler(self, request, exception):
        print "[MQTT ERROR]"
        # print vars(exception)
        # print vars(request)
        pass

    def on_publish(self, client, userdata, mid):
        print("[MQTT] PUBLISHED: "+str(mid))
        pass

    def on_connect(self, client, userdata, flags, rc):
        print("[MQTT] CONNACK received with code %d." % (rc))
        self.connected = True

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        self.active = False
        print("[MQTT] DISCON received with code %d." % (rc))

    def publish(self, channel, message):
        if not self.connected and not self.active:
            self.connect();
        self.client.publish(channel, payload=message, qos=2, retain=True)

    def connect(self):
        self.active = True
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_start()

    def disconnect():
        self.client.disconnect()
        self.client.loop_stop()

# create config file if not already done
if not os.path.exists(config_file):
    cfgfile = open(config_file,'w')
    config = ConfigParser.RawConfigParser()
    config.add_section('web')
    config.set('web', 'configured', False)
    config.set('web', 'host', '0.0.0.0')
    config.set('web', 'port', '5000')
    config.set('web', 'user', '') # leave both blank for no auth
    config.set('web', 'pass', '')
    config.set('web', 'pathprefix', '/xeoma_data_handle') # prefix all requests with this
    config.set('web', 'debug', False)
    config.add_section('mqtt')
    config.set('web', 'host', 'example.com')
    config.set('web', 'port', '1883')
    config.set('web', 'client_id', 'xeoma-mqtt-01')
    config.set('web', 'channel_prefix', 'cameras/')
    config.write(cfgfile)
    cfgfile.close()
    sys.exit("[ERROR] Setup not complete! Update /config/config.ini then set 'configured' under 'web' to False to disable this message.")

config = ConfigParser.ConfigParser()
config.read(config_file)
if not config.getboolean('web', 'configured'):
    sys.exist("[ERROR] Setup not complete! Update /config/config.ini then set 'configured' under 'web' to False to disable this message.")

mqtt = MQTT_Helper(config.get('mqtt', 'client_id'), config.get('mqtt', 'host'), config.get('mqtt', 'port'))
app = Flask(__name__)

def check_auth(username, password):
    global config
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == config.get('web','user') and password == config.get('web','pass')

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    global config
    @wraps(f)
    def decorated(*args, **kwargs):
        global config
        auth = request.authorization
        if config.get('web','pass') and config.get('web','pass') and (not auth or not check_auth(auth.username, auth.password)):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route(config.get('web','pathprefix') + '/<channel>/<msg>')
@requires_auth
def test_page(channel, msg):
    global mqtt,config
    channel = config.get('mqtt','channel_prefix') + str(channel)
    mqtt.publish(channel, str(msg))
    return 'Success! ch:' + str(channel) + ' msg:' + str(msg)

if __name__ == "__main__":
    app.run(debug=config.getboolean('web','debug'),host=config.get('web','host'),port=config.get('web','port'))