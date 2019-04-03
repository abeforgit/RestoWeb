from restoweb import app
from restoweb import models
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/restos', methods=['GET', 'POST'])
def restos():
    if request.method == 'GET':
        resto_list = models.Resto.query.all()
        if request.content_type == 'application/json':
            result = []
            for resto in resto_list:
                result.append({
                    'name': resto.name,
                    'id': url_for('.restos_info', resto_id=resto.id, _external=True)
                })
            return jsonify(restos=result)
        else:
            return render_template("restos.html", resto_list=resto_list)

    elif request.method == 'POST':
        pass


@app.route('/restos/<int:resto_id>', methods=['GET', 'DELETE'])
def restos_info(resto_id):
    if request.method == 'GET':
        resto = models.Resto.query.get_or_404(resto_id)
        schedules = models.Schedule.query.filter_by(resto_id=resto_id).all()

        return render_template("restos_info.html", resto=resto, schedules=schedules)


@app.route('/restos/<int:resto_id>/menus', methods=['GET', 'DELETE'])
def resto_menus(resto_id):
    if request.method == 'GET':
        menus = models.Menu.query.filter_by(resto_id=resto_id)

        return render_template("")


@app.route('/menus', methods=['GET', 'POST'])
def menus():
    pass


@app.route('/menus/<int:menu_id>')
def menus_info(menu_id):
    pass


@app.route('/menus/<int:menu_id>/dishes', methods=['GET', 'POST'])
def menus_dishes(menu_id):
    pass


@app.route('/dishes', methods=['GET', 'POST'])
def dishes():
    pass


@app.route('/dishes/<int:dish_id>', methods=['GET', 'DELETE', 'PUT'])
def dishes_info(dish_id):
    pass
