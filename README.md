places-server
=============

Web server which provide info about places.

##  Install

SOAP web service was tested under Python3.

Install Python3 tools:

* Ubuntu:
```bash
sudo apt-get update
sudo apt-get -y install python3 python3-pip
sudo pip3 install virtualenv
sudo apt-get install libxml2-dev libxslt1-dev python-dev
sudo apt-get install zlib1g-dev
```

* Mac OS X ([brew](http://brew.sh) required):
```bash
sudo brew update
brew install python3
sudo pip3 install virtualenv
```

Clone repository:

```bash
git clone https://github.com/mvidalgarcia/places-server.git
cd places-server
```

Create virtual environment:

```bash
virtualenv venv
```

Activate virtual environment:

```bash
. venv/bin/activate
```

Install dependencies:

```bash
pip3 install -r dependencies
```

Deactivate virtual environment:

```bash
deactivate
```


## Run

Activate virtual environment:

```bash
. venv/bin/activate
```

Run server:
```bash
python3 run.py
```

Deactivate virtual environment:
```bash
deactivate
```
Virtual environment must be activated in order to run the server.
