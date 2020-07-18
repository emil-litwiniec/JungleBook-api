from jungle_book.db import db
from app import app
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@app.before_first_request
def create_db():
    db.create_all()


@manager.command
def drop_all_tables():
    if prompt_bool(
            "Are you sure you want to lose all your data?"):
        try:
            db.drop_all()
        except Exception as e:
            return f'Unable to drop tables: {e}'
        print('[ db ] -> All tables have been dropped')


@manager.command
def create_all_tables():
    if prompt_bool(
            "Are you sure you want to create all tables?"):
        try:
            db.create_all()
        except Exception as e:
            return f'Unable to create all tables: {e}'

        print("[ db ] -> All tables have been successfully created")


if __name__ == '__main__':
    manager.run()
