### service/mysensors_mqtt: interact with a MySensors mqtt broker
## HOW IT WORKS: 
## DEPENDENCIES:
# OS: 
# Python: paho-mqtt
## CONFIGURATION:
# required: "hostname", "port", "subscribe_topic_prefix", "publish_topic_prefix"
# optional: 
## COMMUNICATION:
# INBOUND: 
# - OUT: 
#   required: "node_id", "child_id", "command", "type", "value"
#   optional: 
# OUTBOUND: 
# - controller/hub IN: 
#   required: "node_id", "child_id", "command", "type", "value"
#   optional: 

import paho.mqtt.client as mqtt

from mysensors import Mysensors
from sdk.python.module.helpers.message import Message

import sdk.python.utils.exceptions as exception

class Mysensors_mqtt(Mysensors):
    # What to do when initializing
    def sub_init(self):
        self.required_configuration = ["hostname", "port", "subscribe_topic_prefix", "publish_topic_prefix"]
                
    # transmit a message to a sensor in the radio network
    def tx(self, node_id, child_id, command_string, type_string, payload, ack=0, system_message=False):
        # map the correspoding command and type
        command = self.commands.index(command_string)
        type = self.types[command].index(type_string)
        ack_string = self.acks[ack]
        if not system_message: self.log_info("["+str(node_id)+"]["+str(child_id)+"]["+command_string+"]["+type_string+"] sending message: "+str(payload))
        # publish the payload to the mqtt broker
        topic = self.config["publish_topic_prefix"]+"/"+str(node_id)+"/"+str(child_id)+"/"+str(command)+"/"+str(ack)+"/"+str(type)
        self.log_debug("publishing on topic "+topic+": "+str(payload))
        try: 
            self.gateway.publish(topic, str(payload))
        except Exception,e:
            self.log_error("unable to publish "+str(payload)+" on topic "+topic+": "+exception.get(e))
            
    # connect to the gateway
    def connect(self):
        # receive callback when conneting
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                log_debug("Connected to the MQTT gateway ("+str(rc)+")")
                # subscribe to topic
                self.subscribe_topic(self.config["subscribe_topic_prefix"])
                self.connected = True
            
        # receive a callback when receiving a message
        def on_message(client, userdata, msg):
            try:
                self.log_debug("received "+str(msg.topic)+": "+str(msg.payload))
                # split the topic
                topic, node_id, child_id, command, ack, type = msg.topic.split("/")
            except Exception,e:
                self.log_error("Invalid format ("+msg.topic+"): "+exception.get(e))
                return
            # process the message
            self.process_inbound(int(node_id),int(child_id),int(command),int(ack),int(type),str(msg.payload))
            
        # connect to the gateway
        self.gateway = mqtt.Client()
        try: 
            self.log_info("Connecting to MQTT gateway on "+self.config["hostname"]+":"+str(self.config["port"]))
            password = self.config["password"] if "password" in self.config else ""
            if "username" in self.config: self.gateway.username_pw_set(self.config["username"], password=password)
            self.gateway.connect(self.config["hostname"], self.config["port"], 60)
        except Exception,e:
            self.log_warning("Unable to connect to the MQTT gateway: "+exception.get(e))
            return
        # set callbacks
        self.gateway.on_connect = on_connect
        self.gateway.on_message = on_message
        
    # What to do when running
    def on_start(self):
        self.log_info("Starting mysensors MQTT gateway")
        # request all sensors' configuration so to filter sensors of interest
        self.add_configuration_listener("sensors/#", 1)
        self.connect()
        # start loop (in the background)
        # TODO: reconnect
        try: 
            self.gateway.loop_start()
        except Exception,e: 
            self.log_error("Unexpected runtime error: "+exception.get(e))
    
    # What to do when shutting down
    def on_stop(self):
        self.gateway.loop_stop()
        self.gateway.disconnect()
 
    # subscribe to a mqtt topic
    def subscribe_topic(self, topic):
        self.log_debug("Subscribing to the MQTT topic "+topic)
        self.gateway.subscribe(topic)        
