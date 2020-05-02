import logging
import sys
from datetime import datetime, timedelta
import getInfoSongs

from sanic import Sanic
from sanic.response import json, html, text
from jinja2 import Environment, PackageLoader, select_autoescape
import os


# define the environment for the Jinja2 templates
env = Environment(
    loader=PackageLoader('main', 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl'])
)


# a function for loading an HTML template from the Jinja environment
def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


LOG_FILE = datetime.now().strftime("%Y%m%d") + "logfile.log"

def setLogging():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(LOG_FILE)

    logger.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger

def main(arg1,arg2):
    song1 = arg1
    song2 = arg2

    logger = setLogging()
             
    try:
        if song1=='0':
            raise Exception('Missing first song')
        else:
            if song2=='0':
                raise Exception('Missing second song')
            else:
                relationsDF = getInfoSongs.main(song1,song2,logger)
    except Exception as miss:
        logger.info(miss)

    return relationsDF



# ----------------------------    SECCIÓN DE LA APP Y SUS RUTAS ----------------------------



app = Sanic()

# Serves files from the static folder to the URL /static
app.static('/static', './static')

# Esta es la página principal de la aplicación
@app.route("/")
async def test(request):
    # os.getcwd() devuelve la URL actual
    # template = open(os.getcwd() + "/templates/index.html")
    # return html(template.read())

    # Si el html necesita valores, habría que añadirlos dentro de este template
    # separados por comas. Ej: template('index2.html', var1=var1, var2=var2)
    return template(
        'index2.html'
    )

# Esta es la ruta en la que se muestra nuestro estudio
# Por ahora muestra el dataframe dentro de una tabla,
# se sustituirá por un grafo en una actualización futura
@app.route("/result")
async def test(request):
    thislist = request.query_args # Esta es la lista de argumentos recibidos en la URL

    song1= thislist[0][1]
    song2= thislist[1][1]
    relationsDF = main(song1,song2) # relationsDF es un DataFrame

    return html(relationsDF.to_html())

@app.route("/graph")
async def test(request):

    return template(
        'graph.html'
    )

@app.route("/graph2")
async def test(request):

    return template(
        'graph2.html'
    )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
        debug=bool(os.environ.get('DEBUG', ''))
    )