### service/mysensors_mqtt: interact with a MySensors serial gateway
## HOW IT WORKS: 
## DEPENDENCIES:
# OS: 
# Python: python-serial
## CONFIGURATION:
# required: "port", "baud"
# optional: 
## COMMUNICATION:
# INBOUND: 
# - OUT: 
#   required: "node_id", "child_id", "command", "type", "value"
#   optional: 
# OUTBOUND: 
# - controller/hub IN: 
#   required: "node_id", "child_id", "command", "type"
#   optional: 

import serial

from mysensors import Mysensors
from sdk.python.module.helpers.message import Message

import sdk.python.utils.exceptions as exception

class Mysensors_serial(Mysensors):
    # What to do when initializing
    def sub_init(self):
        self.required_configuration = ["port", "baud"]
                
    # transmit a message to a sensor in the radio network
    def tx(self, node_id, child_id, command_string, type_string, payload, ack=0, system_message=False):
        # map the correspoding command and type
        command = self.commands.index(command_string)
        type = self.types[command].index(type_string)
        ack_string = self.acks[ack]
        if not system_message: self.log_info("["+str(node_id)+"]["+str(child_id)+"]["+command_string+"]["+type_string+"] sending message: "+str(payload))
        # prepare the message
        msg = str(node_id)+";"+str(child_id)+";"+str(command)+";"+str(ack)+";"+str(type)+";"+str(payload)+"\n"
        # send the message through the serial port
        try:
            self.gateway.write(msg)
        except Exception,e:
            self.log_error("unable to send "+str(msg)+" to the serial gateway: "+exception.get(e))
        
    # connect to the gateway
    def connect(self):
        try:
            # connect to the serial gateway
            self.log_info("Connecting to serial gateway on "+self.config["port"]+" with baud rate "+str(self.config["baud"]))
            self.gateway = serial.Serial(self.config["port"],self.config["baud"])
            return True
        except Exception,e:
            self.log_error("Unable to connect to the serial gateway: "+exception.get(e))
            return False
            
    # read a single message from the gateway
    def read(self):
        line = ""
        # read a line
        try:
            line = self.gateway.readline().rstrip()
        except Exception,e:
            self.log_error("Unable to receive data from the serial gateway: "+exception.get(e))
            return None
        return line

