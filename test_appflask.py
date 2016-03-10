from flask import url_for, request

def test_app(client):
	url = url_for('my_form')
	response = client.get(url)
	assert response.status_code == 200
	assert client.get(url_for('my_form')).status_code == 200

def test_myform_get(client):
	url = url_for('my_form_post')
	url2 = url_for('my_form')
	response = client.get(url)
	assert response.status_code == 302
	assert response.headers['Location'] == 'http://localhost/'
	response = client.post(url, data={'artist': 'Dr Dre'})
	assert response.status_code == 200