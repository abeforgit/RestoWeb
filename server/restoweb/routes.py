from restoweb import app


@app.route('/')
def index():
    return "RestoWeb"

