import os
from flask import Flask, render_template, request, g
import logging
from . import logger

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    from . import db
    from . import auth
    db.init_app(app)
    app.register_blueprint(auth.bp)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    @app.route("/index")
    def index():
        logger.log_access('Index')
        return render_template("index.html")
    
    return app
