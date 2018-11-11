from flask_script import Manager

from utils.function import create_app


def main():

    app = create_app()
    app.run('0.0.0.0', port=5555, debug=True)
    # manage.run()


if __name__ == '__main__':
    main()
