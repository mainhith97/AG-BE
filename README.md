# company-api

### Requirements
Mysql 3.5

Python 3.6 or 2.7

### Installation

1. Install packages

    ```
        (for Ubuntu)
        sudo apt-get -y install python-virtualenv mysql-server mysql-client python3 python3-dev python3-pip python-mysqldb libmysqlclient-dev
        (for Window)
        *Install Mysql
    ```

2. Install all dependencies:
    ```
        pip install -r requirements.txt
    ```

3. Init config & database
    ```
        cp src/core/sample.config.env config.env
        cd src
        python manage.py migrate
    ```

4. Start API Server
    ```
        cd src
        python manage.py runserver 127.0.0.1:8001
        http://127.0.0.1:8001/
    ```
