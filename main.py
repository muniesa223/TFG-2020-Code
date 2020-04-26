import logging
import sys
from datetime import datetime, timedelta
import getInfoSongs

from sanic import Sanic
from sanic.response import json, html, text
import os

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

app = Sanic()

# Serves files from the static folder to the URL /static
app.static('/static', './static')

@app.route("/")
async def test(request):
    # os.getcwd() devuelve la URL actual
    template = open(os.getcwd() + "/templates/index.html")
    return html(template.read())

# Esta es la ruta en la que se muestra nuestro estudio
@app.route("/run")
async def test(request):
    song1='Q158553' #satisfaction rolling stones
    song2='Q607742' #hey the beatles
    relationsDF = main(song1,song2) # relationsDF es un DataFrame

    return text(relationsDF)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=os.environ.get('PORT') or 8000,
        debug=True
    ) 