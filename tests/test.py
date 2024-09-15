import pytest
from flask import Flask, Request, Response
import json
from app import app, answer_from_knowledgebase, search_knowledgebase, answer_as_chatbot, handle_request

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_kbanswer(client):
    response = client.post('/kbanswer', json={'message': 'How is pottery made?'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'message' in data

def test_search(client):
    response = client.post('/search', json={'message': 'pottery materials and subjects'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'message' in data

def test_answer(client):
    response = client.post('/answer', json={'message': 'What is a chatbot?'})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'message' in data

def test_bad_request(client):
    response = client.post('/answer', json={'message': ''})
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data

def test_server_error():
    ctx = app.app_context()
    ctx.push()
    request = Request.from_values(headers={'Content-Type': 'application/json'}, data=json.dumps({'message': 'what is pottery?'}), method="POST")
    response = handle_request(request, 'fake_func')
    data = json.loads(response[0].data)
    assert response[1] == 500
    assert 'error' in data

def test_answer_from_knowledgebase():
    message = "What is Python?"
    response_message = answer_from_knowledgebase(message)
    assert isinstance(response_message, str)

def test_search_knowledgebase():
    message = "Python tutorials"
    response_message = search_knowledgebase(message)
    assert isinstance(response_message, str)

def test_answer_as_chatbot():
    message = "What is lambda function in Python?"
    response_message = answer_as_chatbot(message)
    assert isinstance(response_message, str)