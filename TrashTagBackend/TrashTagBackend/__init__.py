from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from TrashTagBackend.config import Config
from flask_cors import CORS
from flask_qrcode import QRcode

db = SQLAlchemy()
qr = QRcode()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	CORS(app)
	qr.init_app(app)
	

	#Import all your blueprints
	from TrashTagBackend.api.routes import api
	from TrashTagBackend.distributor.routes import distributor
	from TrashTagBackend.producer.routes import producer
	from TrashTagBackend.app.routes import app as application

	
	#use the url_prefix arguement if you need prefixes for the routes in the blueprint
	app.register_blueprint(api)
	app.register_blueprint(distributor, url_prefix='/distributor')
	app.register_blueprint(producer, url_prefix='/producer')
	app.register_blueprint(application, url_prefix='/app')


	return app

#Helper function to create database file directly from terminal
def create_database():
	import TrashTagBackend.models
	print("Creating App & Database")
	app = create_app()
	with app.app_context():
		db.create_all()
		db.session.commit()
	print("Successfully Created Database")
