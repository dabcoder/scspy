from flask import Flask, request, render_template, redirect
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy

import os
import datetime
import spotipy
import soundcloud

appf = Flask(__name__)
#Local DB Config
#appf.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/scspy'
#Heroku DB Config
appf.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
appf.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(appf)

from models import Result


@appf.route('/')
def my_form():
    return render_template("index.html")

@appf.route('/songs', methods=['GET','POST'])
def my_form_post():
	if request.method == 'GET':
		return redirect(url_for('my_form'))
	name = request.form['artist']
    #SPOTIFY
	spotify = spotipy.Spotify()
	#SOUNDCLOUD
	client = soundcloud.Client(client_id='SC_Client_ID')

	try:
		#SPOTIFY
		artist = spotify.search(q='artist:' + name, type='artist')
		artist_id = 'spotify:artist:' + str(artist['artists']['items'][0]['external_urls']['spotify'][32:])
		results = spotify.artist_top_tracks(artist_id)
		imgUrl = artist['artists']['items'][0]['images'][2]['url']

		mydict = {}
		mydict2 = {}

		count = 1
		for track in results['tracks'][:10]:
			mydict[count] = track['name']
			count += 1
		top_track = results['tracks'][0]['uri']
		#SOUNDCLOUD
		tracks = client.get('/tracks', q=name)
		for track in tracks:
			mydict2[track.title] = track.permalink_url
		top_trackSC = tracks[0].id

		#Add data to the Postgres DB
		date_r = datetime.datetime.now()
		results_db = Result(
			artist_q=name,
			date_sent=date_r,
		)
		db.session.add(results_db)
		db.session.commit()

		#Returns all the values and serve them in the template
		return render_template('songs.html', data=mydict, data2=mydict2, name=name, img=imgUrl, toptrack=top_track, toptrackSC=top_trackSC)

	except (ValueError, IndexError) as error:
		return render_template('not_found.html')

@appf.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == '__main__':
	appf.run()
