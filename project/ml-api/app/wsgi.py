from .init import create_app
app = create_app()

# Para gunicorn: gunicorn -w 2 -b 0.0.0.0:8000 app.wsgi:app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)