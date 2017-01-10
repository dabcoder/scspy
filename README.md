# scspy

[Search](http://spoticloud.xyz) for an artist or a band's name, it will return:

- Top 10 tracks found on Spotify
- A max of 10 tracks found on SoundCloud

<h2>Local Setup</h2>

1. Clone this repository
2. Create a virtualenv and install the requirements</li>
3. Register an app on SoundCloud via: http://soundcloud.com/you/apps/new</li>  
4. Replace `your_sc_appID` with your actual SoundCloud Client ID  
5. Run the app: `python manage.py runserver`
6. Go to `http://localhost:5000/` and give it a try