Setup:


    python instllation and create virtualenv:
      for mac:    
        brew install python 
        pip install virtualenv
        virtualenv -p /opt/homebrew/bin/python3 ~/venv
      for linux: 
        apt-get install python3
        pip install virtualenv
        virtualenv -p /usr/bin/python3 ~/venv

    activate venv
      source ~/venv/bin/activate
    
    install dependencies
      pip3 install -r requirement.txt
    
    create db if not persent
        touch db.sqlite3
        python3 manage.py makemigrations
        python3 manage.py migrate

    python manage.py runserver
