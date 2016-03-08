from flask import Flask, request, render_template, redirect
from flask import url_for

import spotipy
import soundcloud

appf = Flask(__name__)

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
	client = soundcloud.Client(client_id='my_client_ID')

	try:
		#SPOTIFY
		artist= spotify.search(q='artist:' + name, type='artist')
		artist_id = 'spotify:artist:' + str(artist['artists']['items'][0]['external_urls']['spotify'][32:])
		results = spotify.artist_top_tracks(artist_id)
		imgUrl = artist['artists']['items'][0]['images'][2]['url']

		mydict = {}
		mytab = []

		count = 1
		for track in results['tracks'][:10]:
			mydict[count] = track['name']
			count += 1
		top_track = results['tracks'][0]['uri']
		#SOUNDCLOUD
		tracks = client.get('/tracks', q=name)
		for track in tracks:
			mytab.append(track.title)
		top_trackSC = tracks[0].id
		return render_template('songs.html', data=mydict, data2=mytab, name=name, img=imgUrl, toptrack=top_track, toptrackSC=top_trackSC)

	except (ValueError, IndexError) as error:
		return render_template('not_found.html')

@appf.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == '__main__':
	appf.run()
