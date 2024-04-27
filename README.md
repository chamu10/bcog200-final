# Musical Songs Recommendation
### BCOG200 final project 
## About The Project 
This is a program that suggests you broadway musical songs which have similar tastes with your favorite song.
I made this program because I like broadway musical songs and want to share them with my friends who have little interest in musicals.

## Code Description
First, to use Spotify API, this program makes an authentication by using credential ID and password.

`client = spotipy.Spotify(client_credentials_manager=client_credential)`

Next, when you enter your favortie song in a prompt, this program retrieve track basic information and audio features of the song in spotify.
Also, it retrieves musical songs information.

`result = self.client.search(song_name, type='track') #retrieve basic infomation of song_name`

`fav_song_features = self.client.audio_features(track_id) #retrieve audio features of track_id`

Then, it analyses the similarity between your favorite song and musical songs from numerical perspectives by calculating cosin similarity.

`["acousticness","danceability","energy","id","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","valence"]`

`cosine_similarity(self.musical_song_features, fav_song_features_2D).squeeze()`

Lastly it suggests you top 3 musical songs that have similar tast with your favorite song.

Following is an example. It gives you song name and album name in which the song is collected.

## Using Function
* A function that uses Spotipy to retrieve track id of broadway musical songs and user's favorite song.
* A function that uses Spotipy to retrieve music features of broadway musical songs and user's favorite song.
* A function that uses sklearn library to calculate the song similarity.

## Instruction
1. Run main.py.
2. You are asked to enter your favorite song name. Fill in.
3. You will receive the recommendations for musical songs based on your favorite song.

## Acknowledgments
I refered or used the following sites to make this project.
* [How to Build a Content-Based Song Recommender](https://georgepaskalev.medium.com/how-to-build-a-content-based-song-recommender-4346edbfa5cf)
* [spotify-data-project/Extracting Spotify Audio Features From Spotify Playlist](https://github.com/simon-th/spotify-data-project/blob/master/Extracting%20Spotify%20Audio%20Features.ipynb)
* [Spotify.for Developers](https://developer.spotify.com/documentation/web-api/reference/search)
