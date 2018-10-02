from flask_script import Manager

from utils.functions import create_app


def main():
    app = create_app()
    manage = Manager(app=app)
    manage.run()


if __name__ == '__main__':
    main()
    # app.run(port=8080, host='0.0.0.0',
    #         debug=False)



