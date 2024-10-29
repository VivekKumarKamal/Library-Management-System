from backend.python_files import create_app

app, api = create_app()

if __name__ == '__main__':
    app.run(port=5000)

