places-server
=============

Web server which provides info about places through a SOAP API.

## Functions

### Categories  

| function name              |
|----------------------------|
| get_category(id)           |
| put_category(category)     |
| del_category(id)           |
| del_category_by_name(name) |
|                            | 

### Places  

| function name                                                                    |
|----------------------------------------------------------------------------------|
| get_place(id)                                                                    |
| put_place(place)                                                                 |
| del_place(id)                                                                    |
| get_all_places()                                                                 |
| get_places_by_category_id(category_id,from_id, elements)                         |
| get_near_places_by_category_id(category_id, lat, lng, radius, from_id, elements) |
| gplaces_id_exists_in_category_id(gplaces_id, category_id)                        |
|                                                                                  |


##  Install

SOAP web service was tested under Python3.

Install Python3 tools:

* Ubuntu:
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y install python3 python3-pip
sudo pip3 install virtualenv
sudo apt-get install libxml2-dev libxslt1-dev python-dev
sudo apt-get install zlib1g-dev
```

* Mac OS X ([brew](http://brew.sh) required):
```bash
sudo brew update
sudo apt-get upgrade
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

### places-server

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

### collector

Go to `gplaces` folder:

```bash
cd gplaces
```

Activate virtual environment:

```bash
. venv/bin/activate
```

Run collector:
```bash
python3 collector.py [hours]
```
You can configure the period time of the collector. Default value 6 hours.

Deactivate virtual environment:
```bash
deactivate
```

Note that virtual environment must be activated in order to run both server and collector.  
  
It's recommended using `screen` in order to launch both python files and leave them running.
More information about `screen` in Unix environments [here](https://kb.iu.edu/d/acuy). 
