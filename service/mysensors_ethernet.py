### service/mysensors_mqtt: interact with a MySensors ethernet gateway
## HOW IT WORKS: 
## DEPENDENCIES:
# OS: 
# Python: 
## CONFIGURATION:
# required: "hostname", "port"
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

import socket

from mysensors import Mysensors
from sdk.python.module.helpers.message import Message

import sdk.python.utils.exceptions as exception

class Mysensors_ethernet(Mysensors):
    # What to do when initializing
    def sub_init(self):
        self.required_configuration = ["hostname", "port"]
                
    # transmit a message to a sensor in the radio network
    def tx(self, node_id, child_id, command_string, type_string, payload, ack=0, system_message=False):
        # map the correspoding command and type
        command = self.commands.index(command_string)
        type = self.types[command].index(type_string)
        ack_string = self.acks[ack]
        if not system_message: self.log_info("["+str(node_id)+"]["+str(child_id)+"]["+command_string+"]["+type_string+"] sending message: "+str(payload))
        # prepare the message
        msg = str(node_id)+";"+str(child_id)+";"+str(command)+";"+str(ack)+";"+str(type)+";"+str(payload)+"\n"
        # send the message through the network socket
        try:
            self.gateway.sendall(msg)
        except Exception,e:
            self.log_error("unable to send "+str(msg)+" to the ethernet gateway: "+exception.get(e))
        
    # connect to the gateway
    def connect(self):
        try:
            # connect to the ethernet gateway
            self.log_info("Connecting to ethernet gateway on "+self.config["hostname"]+":"+str(self.config["port"]))
            self.gateway = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.gateway.connect((self.config["hostname"], self.config["port"]))
            return True
        except Exception,e:
            self.log_error("Unable to connect to the ethernet gateway: "+exception.get(e))
            return False
            
    # read a single message from the gateway
    def read(self):
        # read a line
        try:
            line = ""
            while True:
                c = self.gateway.recv(1)
                if c == '\n' or c == '': break
                else: line += c
        except Exception,e:
            self.log_error("Unable to receive data from the ethernet gateway: "+exception.get(e))
            return None
        return line
        
  