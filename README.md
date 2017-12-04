# Security Dashboard

The Security Dashboard (Dashboard from now on) is SHIELD’s topmost component being in charge of enabling users and third party applications to use SHIELD’s internal features. Dashboard is therefore the entry point of SHIELD solution, seamlessly encapsulating the access and use of all its information and features in this component. Being the only point of access for the SHIELD users facilitate the integration and builds a more secure application, since the access control is more robust and protected. Besides integrating with all SHIELD’s components, Dashboard is also responsible for the implementation of a set of support features. It will provide user and tenant management features, billing and monetisation capabilities as well as a remediation subcomponent responsible for persisting and dispatching (upon validation by authorised users) all SHIELD’s remediation suggestions.

# Installation

## Prerequisites

* [Python 3](https://www.python.org/)
* [Eve REST API framework](http://eve.readthedocs.io/en/stable/) which provides (amongst other goodies) [Flask](http://flask.pocoo.org/) for RESTful support, [Cerberus](http://python-cerberus.org/) for JSON validation and [MongoDB](https://www.mongodb.com/) for the actual vNSF & NS data store.
* [RabbitMQ](http://www.rabbitmq.com/) for the messaging server
* [Node](https://nodejs.org/) for the HTTP server
* [AngularJS](https://angularjs.org/) for the web application framework


## Python virtual environment

The [environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) requirements are defined in the [requirements-dashboard.txt](docker/requirements-dashboard.txt) file for the Dashboard API and in the [requirements-dashboard-q.txt](docker/requirements-dashboard-q.txt) file for the Dashboard Queue.

## Docker

### Prerequisites

Install the following packages and versions following the manuals:

* [Docker](https://docs.docker.com/engine/installation/) (17.06.0+)
* [docker-compose](https://docs.docker.com/compose/install/) (3.0+)

Alternatively, install them through the steps below:

```bash
sudo apt-get install --no-install-recommends apt-transport-https curl software-properties-common python-pip
curl -fsSL 'https://sks-keyservers.net/pks/lookup?op=get&search=0xee6d536cf7dc86e2d7d56f59a178ac6c6238f52e' | sudo apt-key add -
sudo add-apt-repository "deb https://packages.docker.com/1.13/apt/repo/ubuntu-$(lsb_release -cs) main"
sudo apt-get update
sudo apt-get -y install docker-engine
sudo pip install docker-compose
```

Finally, add current user to the docker group (allows issuing Docker commands w/o sudo):
```
sudo usermod -G docker $(whoami)
```

### Setup

Automation details can be found in the [DevOps](#devops) section.

TL;DR

* Run it with:

```bash
cd docker
./run.sh --environment .env.production --verbose
```

Once everything is up and running the last lines on the screen should be something like:
```bash
dashboard-gui_1          | Starting up http-server, serving /usr/share/dev/dashboard-gui/dev
dashboard-gui_1          | Available on:
dashboard-gui_1          |   http://127.0.0.1:8080
dashboard-gui_1          |   http://172.18.0.7:8080
dashboard-gui_1          | Hit CTRL-C to stop the server
rev-proxy_1              | [WARNING] 303/174416 (1) : Server BE_dashboard-gui/dashboard-gui is UP.
```

At this point the containers for the message queue server, the recommendations queue logic, the backend API, the recommendations history, the GUI and the reverse proxy are up and running. An example of the docker environment put in place is presented next.

```bash
$ docker ps
CONTAINER ID        IMAGE                          NAMES
32be37213530        docker_msgq                    docker_msgq_1
66df8bf7ec58        docker_dashboard-backend-q     docker_dashboard-backend-q_1
1bc570507e47        docker_dashboard-backend-api   docker_dashboard-backend-api_1
9068b2a54fe1        docker_dashboard-persistence   docker_dashboard-persistence_1
ddd055aa72d2        docker_dashboard-gui           docker_dashboard-gui_1
104d79441a72        docker_rev-proxy               docker_rev-proxy_1
```

Troubleshooting is possible after accessing the container through its name (last column from above):  
`docker exec -it $docker_container_name bash`

### Teardown

To stop the docker environment and teardown everything simply (_in the docker folder_):

```bash
./run.sh --shutdown
```

Please note that this removes all containers so the next time one wants to [setup](#setup) everything it must also perform the [first-time setup](#first-time-setup) procedure.

### First-time setup

The first time the Dashboard environment is set up one must create the data store to hold the Recommendations History data. This is done by:

```bash
docker exec -it docker_dashboard-persistence_1 bash -c "/usr/share/dev/dashboard/docker/setup-datastore.sh --environment .env.production"
```

# Deployment

The default settings deploy the Dashboard GUI in the 80. To ensure the environment is up and running simply open a web browser and head to http://_dashboard_ip_ page. The SHIELD Dashboard web application should be presented.

# Testing

Please read the [Quality Assurance](docs/qa.md) section to grasp how the Dashboard features are validated.

# DevOps

For deployment setup, environments definition and build automation details please  refer to [DevOps](docs/devops.md).

# Further reading

Please refer to the [Dashboard documentation](docs/index.md) for additional insight on how the Dashboard operates and what lies behind the scenes.
