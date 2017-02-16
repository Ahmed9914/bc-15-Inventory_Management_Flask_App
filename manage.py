#!/usr/bin/env python3
from __init__ import app, db
from flask.ext.script import Manager, prompt_bool
from models import Admins, User

#assign manager variable to Manager function with app passesd to it
manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(Admins(username="sAdmin", password="Admin"))
    db.session.add(Admins(username="A", password="A"))
    db.session.add(User(username="u"))
    db.session.commit()
    print('Successfully created the database')

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop the database?"):
        db.drop_all()
        print("Successfully dropped the database")


if __name__ == "__main__":
    manager.run()
