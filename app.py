"""
Archivo principal de la aplicación Flask
"""
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from models import db
from resources.video import Video, VideoList
from config import config
from swagger import spec

def create_app(config_name='default'):
    """
    Función factory para crear la aplicación Flask
    
    Args:
        config_name (str): Nombre de la configuración a utilizar
        
    Returns:
        Flask: Aplicación Flask configurada
    """
    # Crear el objeto 'app'
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    api = Api(app)
    
    # Configurar Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "API de Videos"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Endpoint para especificación OpenAPI
    @app.route('/api/swagger.json')
    def create_swagger_spec():
        return jsonify(spec.to_dict())
    
    # Registrar rutas de la API
    api.add_resource(VideoList, "/api/videos")
    api.add_resource(Video, "/api/videos/<int:video_id>")
    
    return app

if __name__ == "__main__":
    # Obtener configuración del entorno o usar 'development' por defecto
    config_name = os.getenv('FLASK_CONFIG', 'development')
    
    # Crear aplicación
    app = create_app(config_name)
    
    # Crear todas las tablas en la base de datos
    with app.app_context():
        db.create_all()
    
    # Ejecutar servidor
    app.run(host='0.0.0.0', port=5000)

