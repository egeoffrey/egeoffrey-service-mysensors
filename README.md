# egeoffrey-service-mysensors

This is an eGeoffrey service package.

## Description

Interact with a MySensors serial/ethernet/mqtt gateway.

## Install

To install this package, run the following command from within your eGeoffrey installation directory:
```
egeoffrey-cli install egeoffrey-service-mysensors
```
After the installation, remember to run also `egeoffrey-cli start` to ensure the Docker image of the package is effectively downloaded and started.
To validate the installation, go and visit the *'eGeoffrey Admin'* / *'Packages'* page of your eGeoffrey instance. All the modules, default configuration files and out-of-the-box contents if any will be automatically deployed and made available.
## Content

The following modules are included in this package.

For each module, if requiring a configuration file to start, its settings will be listed under *'Module configuration'*. Additionally, if the module is a service, the configuration expected to be provided by each registered sensor associated to the service is listed under *'Service configuration'*.

To configure each module included in this package, once started, click on the *'Edit Configuration'* button on the *'eGeoffrey Admin'* / *'Modules'* page of your eGeoffrey instance.
- **service/mysensors_serial**: interact with a MySensors serial gateway
  - Module configuration:
    - *port**: the serial port the MySensors gateway is attached to (e.g. /dev/mysensors)
    - *baud**: the baud rate to use for communicating with the device (e.g. 9600)
  - Service configuration:
    - Mode 'push':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
    - Mode 'actuator':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
      - *queue_size*: mandatory for sleeping nodes to define how many messages to keep in the queue and send once awake (e.g. 1)
    - Mode 'pull':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
- **service/mysensors_mqtt**: interact with a MySensors MQTT gateway
  - Module configuration:
    - *hostname**: the MQTT hostname to connect to (e.g. egeoffrey-gateway)
    - *port**: the port of the MQTT broker (e.g. 1883)
    - *username*: the username for authenticating against the mqtt broker (e.g. username)
    - *password*: the password for authenticating against the mqtt broker (e.g. password)
    - *subscribe_topic_prefix**: the topic prefix to subscribe to (e.g. mysensors-out)
    - *publish_topic_prefix**: the topic prefix to publish data into (e.g. mysensors-in)
  - Service configuration:
    - Mode 'push':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
    - Mode 'actuator':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
      - *queue_size*: mandatory for sleeping nodes to define how many messages to keep in the queue and send once awake (e.g. 1)
    - Mode 'pull':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
- **service/mysensors_ethernet**: interact with a MySensors ethernet gateway
  - Module configuration:
    - *hostname**: the IP address or hostname running the MySensors gateway (e.g. 192.168.0.230)
    - *port**: the port the gateway is listening to (e.g. 5003)
  - Service configuration:
    - Mode 'push':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
    - Mode 'actuator':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type
      - *queue_size*: mandatory for sleeping nodes to define how many messages to keep in the queue and send once awake (e.g. 1)
    - Mode 'pull':
      - *node_id**: the unique identifier of the node (e.g. 1)
      - *child_id**: each node can have several sensors attached. This is the child-id that uniquely identifies one attached sensor (e.g. 3)
      - *command**: mySensors command to trigger
      - *type**: mySensors type

## Contribute

If you are the author of this package, simply clone the repository, apply any change you would need and run the following command from within this package's directory to commit your changes and automatically push them to Github:
```
egeoffrey-cli commit "<comment>"
```
After taking this action, remember you still need to build (see below) the package (e.g. the Docker image) to make it available for installation.

If you are a user willing to contribute to somebody's else package, submit your PR (Pull Request); the author will take care of validating your contributation, merging the new content and building a new version.

## Build

Building is required only if you are the author of the package. To build a Docker image and automatically push it to [Docker Hub](https://hub.docker.com/r/egeoffrey/egeoffrey-service-mysensors), run the following command from within this package's directory:
```
egeoffrey-cli build egeoffrey-service-mysensors
```
To function properly, when running in a Docker container, the following additional configuration settings has to be added to e.g. your docker-compose.yml file (when installing through egeoffrey-cli, this is not needed since done automatically upon installation):
```
devices:
- /dev/ttyAMA0:/dev/ttyAMA0
```

## Uninstall

To uninstall this package, run the following command from within your eGeoffrey installation directory:
```
egeoffrey-cli uninstall egeoffrey-service-mysensors
```
Remember to run also `egeoffrey-cli start` to ensure the changes are correctly applied.
## Tags

The following tags are associated to this package:
```
service mysensors mqtt serial
```

## Version

The version of this egeoffrey-service-mysensors is 1.0-19 on the master branch.
