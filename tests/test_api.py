import json
import pytest

from app import create_app
from models import db
from models.video import VideoModel


@pytest.fixture
def client():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_put_get_patch_delete_flow(client):
    # Crear video
    payload = {"name": "Test Video", "views": 10, "likes": 2}
    resp = client.put('/api/videos/1', json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['id'] == 1
    assert data['name'] == "Test Video"

    # Obtener video
    resp = client.get('/api/videos/1')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['views'] == 10

    # Actualizar video
    resp = client.patch('/api/videos/1', json={"views": 50})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['views'] == 50

    # Eliminar video
    resp = client.delete('/api/videos/1')
    assert resp.status_code == 204

    # Obtener video eliminado
    resp = client.get('/api/videos/1')
    assert resp.status_code == 404


def test_put_conflict(client):
    payload = {"name": "A", "views": 1, "likes": 0}
    resp = client.put('/api/videos/2', json=payload)
    assert resp.status_code == 201
    # Intentar crear de nuevo con mismo id
    resp = client.put('/api/videos/2', json=payload)
    assert resp.status_code == 409


def test_get_video_list(client):
    # Crear varios videos para probar paginación
    for i in range(1, 15):
        payload = {
            "name": f"Video {i}",
            "views": i * 100,
            "likes": i * 10
        }
        client.put(f'/api/videos/{i}', json=payload)
    
    # Probar primera página (default: 10 items)
    resp = client.get('/api/videos')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['items']) == 10
    assert data['page'] == 1
    assert data['total'] == 14
    assert data['pages'] == 2
    
    # Probar segunda página con tamaño personalizado
    resp = client.get('/api/videos?page=2&per_page=5')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['items']) == 5
    assert data['page'] == 2
    assert data['per_page'] == 5
