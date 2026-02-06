import os
import mongomock


class Config():
    """Classe base de configuração"""
    pass


class DevConfig():

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'username': os.getenv('MONGODB_USER'),
        'password': os.getenv('MONGODB_PASSWORD'),
        # 'port': 27017,
        # 'authentication_source': 'admin'
    }


class ProdConfig:
        
    MONGODB_USER = os.getenv('MONGODB_USER')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    MONGODB_HOST = os.getenv('MONGODB_HOST')
    MONGODB_DB = os.getenv('MONGODB_DB')

    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://%s:%s@%s/%s' % (
            MONGODB_USER,
            MONGODB_PASSWORD,
            MONGODB_HOST,
            MONGODB_DB
        )
    }



class MockConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'users',
        'host': 'localhost',
        'port': 27017,
        'mongo_client_class': mongomock.MongoClient
    }

