"""
Configuración y especificación de Swagger/OpenAPI
"""
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import jsonify, render_template
from marshmallow import Schema, fields

# Esquemas para la documentación
class VideoSchema(Schema):
    id = fields.Int(required=True, description="ID único del video")
    name = fields.Str(required=True, description="Nombre o título del video")
    views = fields.Int(required=True, description="Número de vistas")
    likes = fields.Int(required=True, description="Número de likes")

class PaginationSchema(Schema):
    items = fields.List(fields.Nested(VideoSchema), description="Lista de videos en la página actual")
    page = fields.Int(description="Número de página actual")
    per_page = fields.Int(description="Elementos por página")
    total = fields.Int(description="Total de videos")
    pages = fields.Int(description="Total de páginas")

# Crear especificación
spec = APISpec(
    title="API de Videos",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="API RESTful para gestión de videos"),
    plugins=[MarshmallowPlugin()],
)

# Registrar esquemas
spec.components.schema("Video", schema=VideoSchema)
spec.components.schema("PaginatedVideos", schema=PaginationSchema)

# Documentación de endpoints
spec.path(
    path="/api/videos",
    operations={
        "get": {
            "summary": "Obtiene una lista paginada de videos",
            "description": "Retorna una lista de videos con paginación",
            "parameters": [
                {
                    "name": "page",
                    "in": "query",
                    "description": "Número de página",
                    "schema": {"type": "integer", "default": 1}
                },
                {
                    "name": "per_page",
                    "in": "query",
                    "description": "Elementos por página",
                    "schema": {"type": "integer", "default": 10, "maximum": 50}
                }
            ],
            "responses": {
                "200": {
                    "description": "Lista paginada de videos",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PaginatedVideos"}
                        }
                    }
                }
            }
        }
    }
)

spec.path(
    path="/api/videos/{video_id}",
    operations={
        "get": {
            "summary": "Obtiene un video por ID",
            "parameters": [
                {
                    "name": "video_id",
                    "in": "path",
                    "required": True,
                    "description": "ID del video",
                    "schema": {"type": "integer"}
                }
            ],
            "responses": {
                "200": {
                    "description": "Video encontrado",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Video"}
                        }
                    }
                },
                "404": {
                    "description": "Video no encontrado"
                }
            }
        },
        "put": {
            "summary": "Crea un nuevo video",
            "parameters": [
                {
                    "name": "video_id",
                    "in": "path",
                    "required": True,
                    "description": "ID para el nuevo video",
                    "schema": {"type": "integer"}
                }
            ],
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Video"}
                    }
                }
            },
            "responses": {
                "201": {
                    "description": "Video creado",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Video"}
                        }
                    }
                },
                "409": {
                    "description": "El ID ya existe"
                }
            }
        },
        "patch": {
            "summary": "Actualiza un video existente",
            "parameters": [
                {
                    "name": "video_id",
                    "in": "path",
                    "required": True,
                    "description": "ID del video a actualizar",
                    "schema": {"type": "integer"}
                }
            ],
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "views": {"type": "integer", "minimum": 0},
                                "likes": {"type": "integer", "minimum": 0}
                            }
                        }
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Video actualizado",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Video"}
                        }
                    }
                },
                "404": {
                    "description": "Video no encontrado"
                }
            }
        },
        "delete": {
            "summary": "Elimina un video",
            "parameters": [
                {
                    "name": "video_id",
                    "in": "path",
                    "required": True,
                    "description": "ID del video a eliminar",
                    "schema": {"type": "integer"}
                }
            ],
            "responses": {
                "204": {
                    "description": "Video eliminado"
                },
                "404": {
                    "description": "Video no encontrado"
                }
            }
        }
    }
)