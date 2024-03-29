import pandas
import spotify
from spotipy.oauth2 import SpotifyClientCredentials
import json

class Data:
	def __init__(self, fav_song):
		self.fav_song = fav_song # inputed song
		self.client = None # Spotify client information
		self.fav_song_info = None # features of favorited song
		self.musical_song_info_list = None # features of musical songs


		self.get_client()
		fav_song_name = self.ask_fav_song()
		self.fav_song_info = self.get_song_features(fav_song_name)
		self.musical_song_info_list = self.get_musical_features()

	def get_client(self):
		client_id = input("Enter your Spotify client ID:")
		client_secret = input("Enter your Spotify client secret:")
		client_credential = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
		self.client = spotipy.Spotify(client_credentials_manager=client_credential)

	def search_song_track(self, song_name):
		result = slef.client.search(song_name, type='track')
		track_data = result["tracks"]["items"]
		return track_data

	def get_song_features(self, song_name):
		track_id = self.search_song_track(song_name)["id"]
		features = self.client.audio_features(track_id)
		return features

	def ask_fav_song(self):
		song_name = input("Enter your favorite song name: ")
		return song_name

	def get_musical_features(self):
		musical_results = slef.client.search(q = "genre: musical", type='track')
		features_list = []
		for track in musical_results["tracks"]["items"]:
			song_feature = self.client.audio_features(track["id"])
			features_list.append(song_feature)
		retune features_list




