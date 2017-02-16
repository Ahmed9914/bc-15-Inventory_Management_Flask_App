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
    db.session.add(Admins(username="Robin", password="1"))
    db.session.add(Admins(username="Joe", password="1"))
    db.session.add(Admins(username="Sharon", password="1"))
    db.session.add(Admins(username="Eze", password="1"))
    db.session.add(Admins(username="JXN", password="1"))
    db.session.add(User(username="csharon"))
    db.session.add(User(username="kkevin"))
    db.session.add(User(username="jokal"))
    db.session.add(User(username="ahart"))
    db.session.add(User(username="bscott"))
    db.session.add(User(username="mherbert"))
    db.session.commit()
    print('Successfully created the database')

@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop the database?"):
        db.drop_all()
        print("Successfully dropped the database")


if __name__ == "__main__":
    manager.run()
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
