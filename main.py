from website import create_app

app = create_app()

#running file: if import main.py from another file without this line, it would run the webserver
#makes sure you run the web server after running this file.
if __name__ == '__main__':
    app.run(debug=True, port=5001)
