from .app import app

client = app.test_client()


def test_get_tutorials():
    res = client.get('/tutorials')
    assert res.status_code == 200
    assert len(res.get_json()) == 2
    assert res.get_json()[0]['id'] == 1


def test_post_tutorial():
    tutorial = {
        'id': 3,
        'title': 'title3',
        'description': 'descriprion3'
    }
    res = client.post('/tutorials', json=tutorial)
    assert res.status_code == 200
    assert len(res.get_json()) == 3
    assert res.get_json()[2]['id'] == 3


def test_put_tutorial():
    params = {
        'title': 'title4',
        'description': 'descriprion4'
    }
    res = client.put('/tutorials/1', json=params)
    assert res.status_code == 200
    assert len(res.get_json()) == 3
    assert res.get_json()['title'] == params['title']


def test_delete_tutorial():
    res = client.delete('/tutorials/3')
    assert res.status_code == 204
