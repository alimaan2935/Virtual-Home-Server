import configparser
import paho.mqtt.client as mqtt
import random
import time


# Name of this client. Don't use identical client IDs for different clients
clientID='mac'
DEBUG = 0


# Subscribe to topic with unique identifier. This is where the
# response will be sent by the service.
requestTopic  = 'services/timeservice/request/'         # Request goes here. Request ID will be appended later
responseTopic = 'services/timeservice/response/'        # Response comes here. Request ID will be appended later


#
# Callback that is executed when the client receives a CONNACK response from the server.
#
def onConnect(client, userdata, flags, rc):
   print("Connected with result code " + str(rc))

#
# Callback that is executed when subscribing to a topic
#
def onSubscribe(client, userdata, mid, granted_qos):
   if DEBUG: print('Subscribed on topic.')


#
# Callback that is executed when a message is received.
# This displays the time from the remote service.
#
def onMessage(client, userdata, message):
   # Decode the payload to get rid of the 'b' prefix and single quotes:
   print('It is ' + str(message.payload.decode("utf-8")))


#
# Callback that is executed when we disconnect from the broker.
#
def onDisconnect(client, userdata, message):
   print("Disconnected from the broker.")


#-----------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------


# Create MQTT client instance
mqttc = mqtt.Client(client_id=clientID, clean_session=True)


# Define the callback functions
mqttc.on_connect    = onConnect
mqttc.on_subscribe  = onSubscribe
mqttc.on_message    = onMessage
mqttc.on_disconnect = onDisconnect


# Connect to the broker
mqttc.connect("192.168.2.15", port=1883, keepalive=60, bind_address="")
mqttc.loop_start()


#
# Keep looping, asking for the time every <n> seconds.
#
while True:
   requestID = str(random.randrange(10000))     # Create a new random request (topic) ID

   # Subscribe to the topic where we expect the response
   mqttc.subscribe(responseTopic+requestID, 0)    # topic name, QoS

   # Publish time request on request topic
   # Note that we sent no payload in the request
   mqttc.publish(requestTopic+requestID, qos=0, retain=False)

   time.sleep(2)        # blocking sleep, 2 seconds

   # Unsubscribe from the temporary topics
   mqttc.unsubscribe(responseTopic+requestID)
   mqttc.unsubscribe(requestTopic+requestID)


# Clean up when done
mqttc.loop_stop()
mqttc.disconnect()

# End

