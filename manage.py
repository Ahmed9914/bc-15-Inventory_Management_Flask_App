#!/usr/bin/env python3
from __init__.py import app
from flask.ext.script import Manager

#assign manager variable to Manager function with app passesd to it
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
