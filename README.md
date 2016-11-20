# scspy

https://scspy.herokuapp.com/ 

Search for an artist or a band's name, it will return:

- Top 10 tracks found on Spotify
- A max of 10 tracks found on SoundCloud

<h2>Local Setup</h2>

1. Clone this repository
2. Create a virtualenv and install the requirements</li>
3. Register an app on SoundCloud via: http://soundcloud.com/you/apps/new</li>
4. Setup a Database locally
5. Export the variables DATABASE_URL and SC_CLIENT_ID. `export DATABASE_URL=...` and `export SC_CLIENT_ID=...`
6. Run the app: `python manage.py runserver`
7. Go to `http://localhost:5000/` and give it a try
