from webapp import app
from sys import argv

if __name__ == '__main__':
    if len(argv) == 2:
        app.run(debug=True, host=argv[1])
    else:
        app.run(debug=True, host='192.168.0.102')
