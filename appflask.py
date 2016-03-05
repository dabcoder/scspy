from flask import Flask, request, render_template

import spotipy
import soundcloud

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")

@app.route('/songs', methods=['GET','POST'])
def my_form_post():
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

		mydict = {}
		mytab = []

		count = 1
		for track in results['tracks'][:10]:
			mydict[count] = track['name']
			count += 1
		#SOUNDCLOUD
		tracks = client.get('/tracks', q=name)
		for track in tracks:
			mytab.append(track.title)
		return render_template('songs.html', data=mydict, data2=mytab, name=name)

	except (ValueError, IndexError) as error:
		return render_template('not_found.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == '__main__':
	app.run()
