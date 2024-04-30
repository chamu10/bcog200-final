# Musical Songs Recommendation
### BCOG200 final project 
## About The Project 
This is a program that suggests you broadway musical songs which have similar tastes with your favorite song.
I made this program because I like broadway musical songs and want to share them with my friends who have little interest in musicals.

## Code Description
* First, to use Spotify API, this program makes an authentication by using credential ID and password.

  `client = spotipy.Spotify(client_credentials_manager=client_credential)`

* Next, when you enter your favortie song in a prompt, this program retrieve basic information and audio features of the song in spotify.
At the same time, it retrieves musical songs information.

  `result = self.client.search(song_name, type='track') #retrieve basic infomation of song_name`

  `fav_song_features = self.client.audio_features(track_id) #retrieve audio features of track_id`

* Then, it analyses the similarity between your favorite song and musical songs from numerical perspectives by calculating cosin similarity.

  `["acousticness","danceability","energy","id","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","valence"]`

  `cosine_similarity(self.musical_song_features, fav_song_features_2D).squeeze()`

* Lastly it suggests you top 3 musical songs that have similar taste with your favorite song.

* Following is an example. It gives you song name and album name.
  ![image](https://github.com/chamu10/bcog200-final/assets/90808614/860e64ba-7a24-422c-8a95-aa7b8401d430)

## Using Function
* A function that uses Spotipy to retrieve track id of broadway musical songs and user's favorite song.
* A function that uses Spotipy to retrieve music features of broadway musical songs and user's favorite song.
* A function that uses sklearn library to calculate the song similarity.

## Instruction
1. Create your Spotify API account.
   - This program uses Spotify API so you need your Spotify client ID and credential. Creating and using API is free. 
   - Refer to this website. [Getting Started with Spotify's API&Spotify](https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b)
     - If you do not have Spotify account, first create your Spotify account. Next, follow the below instruction. 
     - If you have Spotify account, go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and click "create an app." Then, you are provided with your client ID and credential.
2. Download main.py and save it in your local file.
3. Insatll pandas, spotify, and scikit-learn packages.

    `pip install pandas spotify scikit-learn`

4. Move to where you save main.py and run it.

    `python3.12 main.py`

5. You are asked to enter your Spotify client ID, Spotify client secret and favorite song name. Fill in.
6. You will receive the recommendations for musical songs based on your favorite song.

## Acknowledgments
I refered or used the following sites to make this project.
* [How to Build a Content-Based Song Recommender](https://georgepaskalev.medium.com/how-to-build-a-content-based-song-recommender-4346edbfa5cf)
* [spotify-data-project/Extracting Spotify Audio Features From Spotify Playlist](https://github.com/simon-th/spotify-data-project/blob/master/Extracting%20Spotify%20Audio%20Features.ipynb)
* [Spotify.for Developers](https://developer.spotify.com/documentation/web-api/reference/search)
* [Getting Started with Spotify's API&Spotify](https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b)
