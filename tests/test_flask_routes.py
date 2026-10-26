"""HTTP integration for isolated calculator blueprint without requiring sensor stream."""
import pytest
flask = pytest.importorskip('flask')
from capstone.routes import bp

@pytest.fixture
def client():
    application=flask.Flask(__name__)
    application.register_blueprint(bp)
    return application.test_client()


def test_tank_web_page(client):
    response=client.get('/tank')
    assert response.status_code==200
    assert b'Tank Fill Calculator' in response.data


def test_http_valid_and_unit_conversion(client):
    r=client.post('/api/tank-volume',json={'length_ft':10,'width_ft':6,'fill_depth':2.5,'depth_unit':'ft'})
    assert r.status_code==200
    assert r.json['volume_gallons']==pytest.approx(1122.078)


def test_http_reject_unsupported_unit(client):
    r=client.post('/api/tank-volume',json={'length_ft':10,'width_ft':6,'fill_depth':2.5,'depth_unit':'cm'})
    assert r.status_code==422 and 'depth_unit' in r.json['error']


def test_http_reject_missing_depth_unit(client):
    r=client.post('/api/tank-volume',json={'length_ft':10,'width_ft':6,'fill_depth':2.5})
    assert r.status_code==400 and 'depth_unit' in r.json['error']


def test_http_all_runs_correct(client):
    body={'runs':[{'run_id':'R-103','length_ft':10,'width_ft':6,'fill_depth':12,'depth_unit':'in'},
                  {'run_id':'R-116','length_ft':12,'width_ft':5,'fill_depth':22,'depth_unit':'in'}]}
    r=client.post('/api/tank-total',json=body)
    assert r.status_code==200
    assert r.json['total_gallons']==pytest.approx(1271.6884)
