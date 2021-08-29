import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = "Hard to guess String"
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = "your email address"
	MAIL_PASSWORD = "your password"
	FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"
	FLASKY_MAIL_SENDER = "Flasky Admin <email address>"
	FLASKY_ADMIN = "your email administrator/address"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or "sqlite:///" + os.path.join(basedir,"data-dev.sqlite")


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir,"data-dev.sqlite")


config = {
	"development" : DevelopmentConfig,
	"testing" : TestingConfig,
	"production" : ProductionConfig,
	"default" : DevelopmentConfig
}
