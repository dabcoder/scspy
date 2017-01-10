from flask import Flask, request, render_template, redirect
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from healthcheck import HealthCheck, EnvironmentDump


import os
import datetime
import urllib
import spotipy
import soundcloud

appf = Flask(__name__)
appf.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
appf.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(appf)
client = soundcloud.Client(client_id=your_sc_appID)

from models import Result

#Index page
@appf.route('/')
def my_form():
    return render_template("index.html")

#Get songs
@appf.route('/songs', methods=['GET','POST'])
def my_form_post():
	if request.method == 'GET':
		return redirect(url_for('my_form'))
	name = request.form['artist'].lstrip()
    #SPOTIFY
	spotify = spotipy.Spotify()
	#SOUNDCLOUD

	try:
		#SPOTIFY
		artist = spotify.search(q='artist:' + name, type='artist')
		artist_id = 'spotify:artist:' + str(artist['artists']['items'][0]['external_urls']['spotify'][32:])
		results = spotify.artist_top_tracks(artist_id)
		imgUrl = artist['artists']['items'][0]['images'][2]['url']
		related = spotify.artist_related_artists(artist_id)

		spotify_song_list = {}
		soundcloud_song_list = {}
		recommended_l = []
		count = 1
		for track in results['tracks'][:10]:
			spotify_song_list[count] = track['name']
			count += 1
		top_track = results['tracks'][0]['uri']
		for artist_related in related['artists'][:10]:
			recommended_l.append(artist_related['name'])
		recommendations = [unicode(x).decode('utf8') for x in recommended_l]
		#SOUNDCLOUD
		tracks = client.get('/tracks', q=name)
		if tracks != []:
			for track in tracks:
				soundcloud_song_list[track.title] = "https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/" + str(track.id)
			#For the SoundCloud widget
			top_trackSC = tracks[0].id
		else:
			soundcloud_song_list = 0
			top_trackSC = 0
			print soundcloud_song_list, top_trackSC
		try:
			#Add data to the Postgres DB
			date_r = datetime.datetime.now()
			results_db = Result(
				artist_q=name,
				date_sent=date_r,
			)
			db.session.add(results_db)
			db.session.commit()
		except:
			print "Unable to insert in the database"
		#Returns all the values and serve them in the template
		return render_template('songs.html', sp_data=spotify_song_list, sc_data=soundcloud_song_list, name=name, img=imgUrl, toptrack=top_track, toptrackSC=top_trackSC, recom=recommendations)

	except (ValueError, IndexError) as error:
		print error
		return render_template('not_found.html')

#Get list of queries, stored in Postgres
@appf.route('/dbqueries', methods=['GET'])
def get_queries():
	results_queries = []
	result_entry = {}
	try:
		result_a = db.session.execute("SELECT * FROM results;")
		for e in result_a:
			result_entry['artist'] = e.artist_q
			result_entry['date'] = e.date_sent
			results_queries.append(result_entry.copy())
		return render_template('dbqueries.html', data=results_queries)
	except:
		print "Something went wrong!"		

@appf.errorhandler(500)
def page_not_found(e):
	return render_template('500.html')

if __name__ == '__main__':
	appf.run()
