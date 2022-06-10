import pytest
from bson import ObjectId
import datetime
from fastapi.testclient import TestClient

from main import app
from config.db import conn

TEST_CHAT = {
    '_id': ObjectId('625c9dcd232be00e5f827f6a'),
    'users': [
        'user_1',
        'user_2'
    ],
    'messages': [
        {
            'sender': 'user_1',
            'text': 'hello',
            'time': datetime.datetime.today()
        }
    ],
    'date_created': datetime.datetime.today()
}

client = TestClient(app)


@pytest.fixture()
def mongo_test_empty():
    conn.chats.delete_many({})


@pytest.fixture()
def mongo_test(mongo_test_empty):
    conn.chats.insert_one(TEST_CHAT)


def test_get_all_chats_empty(mongo_test_empty):
    response = client.get('/chats', headers={'x-user-id': 'user 1'})
    assert response.status_code == 200
    assert response.json() == []


def test_not_sending_user_id_fails(mongo_test_empty):
    response = client.get('/chats')
    assert response.status_code == 400
    assert response.json() == {'detail': 'Missing x-user-id'}


def test_create_chat(mongo_test):
    test_chat = {'user': 'user 2'}
    response = client.post('/chats', json=test_chat, headers={'x-user-id': 'user 1'})
    assert response.status_code == 201
    assert len(response.json()) > 0
    assert set(response.json()['users']) == {'user 1', 'user 2'}
    assert response.json()['messages'] == []
    assert 'id' in response.json()
    assert 'date_created' in response.json()


def test_get_all_chats(mongo_test):
    for i in range(10):
        test_chat = {'user': f'user {i + 2}'}
        client.post('/chats', json=test_chat, headers={'x-user-id': 'user 1'})
    response = client.get('/chats', headers={'x-user-id': 'user 1'})
    assert response.status_code == 200
    assert len(response.json()) == 10

    response = client.get('/chats', headers={'x-user-id': 'user 2'})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_chat_not_found(mongo_test):
    chat_id = '625c9dcd232be00e5f827f7b'
    response = client.get('/chats/{}'.format(chat_id), headers={'x-user-id': 'user 1'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Chat {} not found'.format(chat_id)}


def test_get_chat_not_found_if_not_owner(mongo_test_empty):
    test_chat = {'user': 'user 2'}
    response = client.post('/chats', json=test_chat, headers={'x-user-id': 'user 1'})
    assert response.status_code == 201

    chat_id = response.json()['id']
    response = client.get('/chats/{}'.format(chat_id), headers={'x-user-id': 'user 1'})
    assert response.status_code == 200

    response = client.get('/chats/', headers={'x-user-id': 'user 1'})
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get('/chats/{}'.format(chat_id), headers={'x-user-id': 'user 2'})
    assert response.status_code == 200

    response = client.get('/chats/{}'.format(chat_id), headers={'x-user-id': 'user 3'})
    assert response.status_code == 400
    assert response.json() == {'detail': 'The owner of chat {} is not {}'.format(chat_id, 'user 3')}

    response = client.get('/chats/', headers={'x-user-id': 'user 3'})
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_chat(mongo_test):
    response = client.get('/chats/{}'.format(str(TEST_CHAT['_id'])), headers={'x-user-id': TEST_CHAT['users'][0]})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['date_created']
    assert json_response['id'] == str(TEST_CHAT['_id'])
    assert json_response['users'] == TEST_CHAT['users']
    assert len(json_response['messages']) == len(TEST_CHAT['messages'])


def test_add_message(mongo_test):
    new_msg = {'message': 'a test message'}
    response = client.put('/chats/{}/message'.format(str(TEST_CHAT['_id'])), json=new_msg,
                          headers={'x-user-id': TEST_CHAT['users'][1]})
    assert response.status_code == 200
    assert response.json()['id'] == str(TEST_CHAT['_id'])
    assert response.json()['users'] == TEST_CHAT['users']
    assert len(response.json()['messages']) == len(TEST_CHAT['messages']) + 1
    test_messages = TEST_CHAT['messages'].copy()
    test_messages.append({
        'text': new_msg['message'],
        'sender': TEST_CHAT['users'][1],
        'time': datetime.datetime.today()
    })
    for i, m in enumerate(response.json()['messages']):
        assert m['text'] == test_messages[i]['text']


# def test_update_chat_not_found_fails(mongo_test_empty):
#     updated_chat = {'name': 'updated_name', 'artists': ['updated_artist']}
#     response = client.put('/chats/{}'.format(str(TEST_SONG['_id'])), json=updated_chat,
#                           headers={'x-user-id': TEST_ARTIST['user_id']})
#     assert response.status_code == 404
#
#
# def test_delete_chat(mongo_test):
#     response = client.delete('/chats/{}'.format(TEST_SONG['_id']),
#                              headers={'x-user-id': TEST_ARTIST['user_id']})
#     assert response.status_code == 204
#     response_get = client.get('/chats/{}'.format(TEST_SONG['_id']),
#                               headers={'x-user-id': TEST_ARTIST['user_id']})
#     assert response_get.status_code == 404
#
#
# def test_delete_chat_not_found_fails(mongo_test_empty):
#     response = client.delete('/chats/{}'.format(TEST_SONG['_id']),
#                              headers={'x-user-id': TEST_ARTIST['user_id']})
#     assert response.status_code == 404
#
#
# def test_get_invalid_id_fails(mongo_test):
#     response_get = client.get('/chats/{}'.format('123'))
#     assert response_get.status_code == 400
