from flask_script import Manager

from utils.functions import create_app


def main():

    app = create_app()
    manage = Manager(app=app)


    manage.run()

if __name__ == '__main__':
    main()