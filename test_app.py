import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data

@patch('app.get_db_connection')
@patch('database.return_db_connection')
def test_airports_endpoint(mock_return_db_conn, mock_get_db_conn, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        ("Henri Coandă Airport", "Bucharest", "OTP", "Romania"),
        ("Heathrow Airport", "London", "LHR", "UK"),
    ]

    mock_conn.cursor.return_value = mock_cursor
    mock_get_db_conn.return_value = mock_conn

    response = client.get('/airports')
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['IATA Code'] == "OTP"
