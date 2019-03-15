from restoweb import app


@app.errorhandler(404)
def error404(error):
    return "<h1>Custom 404</h1>"
