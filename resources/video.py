"""
Recursos y rutas para la API de videos
"""
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from models.video import VideoModel
from models import db

# Campos para serializar respuestas
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Parser para los argumentos de paginación
video_list_args = reqparse.RequestParser()
video_list_args.add_argument("page", type=int, help="Número de página", default=1)
video_list_args.add_argument("per_page", type=int, help="Elementos por página", default=10)

# Campos para la respuesta paginada
pagination_fields = {
    'items': fields.List(fields.Nested(resource_fields)),
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total': fields.Integer,
    'pages': fields.Integer
}

# Parser para los argumentos en solicitudes PUT (crear video)
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Nombre del video es requerido", required=True)
video_put_args.add_argument("views", type=int, help="Número de vistas del video", required=True)
video_put_args.add_argument("likes", type=int, help="Número de likes del video", required=True)

# Parser para los argumentos en solicitudes PATCH (actualizar video)
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Nombre del video")
video_update_args.add_argument("views", type=int, help="Número de vistas del video")
video_update_args.add_argument("likes", type=int, help="Número de likes del video")

def abort_if_video_doesnt_exist(video_id):
    """
    Verifica si un video existe, y si no, aborta la solicitud
    
    Args:
        video_id (int): ID del video a verificar
    """
    video = VideoModel.query.filter_by(id=video_id).first()
    if not video:
        abort(404, message=f"No se encontró un video con el ID {video_id}")
    return video

class Video(Resource):
    """
    Recurso para gestionar videos individuales
    
    Métodos:
        get: Obtener un video por ID
        put: Crear un nuevo video
        patch: Actualizar un video existente
        delete: Eliminar un video
    """
    
    @marshal_with(resource_fields)
    def get(self, video_id):
        """
        Obtiene un video por su ID
        
        Args:
            video_id (int): ID del video a obtener
            
        Returns:
            VideoModel: El video solicitado
        """
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message=f"No se encontró un video con el ID {video_id}")
        return video
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        """
        Crea un nuevo video con un ID específico
        
        Args:
            video_id (int): ID para el nuevo video
            
        Returns:
            VideoModel: El video creado
        """
        # Verificar que no exista ya
        existing = VideoModel.query.filter_by(id=video_id).first()
        if existing:
            abort(409, message=f"Ya existe un video con el ID {video_id}")

        args = video_put_args.parse_args()
        # Validaciones básicas
        name = args.get('name')
        views = args.get('views')
        likes = args.get('likes')

        if views is None or likes is None or name is None:
            abort(400, message="Campos 'name', 'views' y 'likes' son requeridos")
        if views < 0 or likes < 0:
            abort(400, message="'views' y 'likes' deben ser enteros no negativos")

        video = VideoModel(id=video_id, name=name, views=views, likes=likes)
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        """
        Actualiza un video existente
        
        Args:
            video_id (int): ID del video a actualizar
            
        Returns:
            VideoModel: El video actualizado
        """
        video = abort_if_video_doesnt_exist(video_id)
        args = video_update_args.parse_args()

        if args.get('name') is not None:
            video.name = args.get('name')
        if args.get('views') is not None:
            if args.get('views') < 0:
                abort(400, message="'views' debe ser un entero no negativo")
            video.views = args.get('views')
        if args.get('likes') is not None:
            if args.get('likes') < 0:
                abort(400, message="'likes' debe ser un entero no negativo")
            video.likes = args.get('likes')

        db.session.commit()
        return video
    
    def delete(self, video_id):
        """
        Elimina un video existente
        
        Args:
            video_id (int): ID del video a eliminar
            
        Returns:
            str: Mensaje vacío con código 204
        """
        video = abort_if_video_doesnt_exist(video_id)
        db.session.delete(video)
        db.session.commit()
        return '', 204


class VideoList(Resource):
    """
    Recurso para listar videos con paginación
    """
    @marshal_with(pagination_fields)
    def get(self):
        """
        Obtiene una lista paginada de videos
        
        Returns:
            dict: Lista paginada de videos con metadatos
        """
        args = video_list_args.parse_args(strict=True)
        page = max(1, args.get('page', 1))
        per_page = min(50, max(1, args.get('per_page', 10)))
        
        # Obtener videos paginados ordenados por id
        query = VideoModel.query.order_by(VideoModel.id)
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'items': pagination.items,
            'page': pagination.page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }

