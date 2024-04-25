<<<<<<< HEAD
import pandas as pd
#import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.metrics.pairwise import cosine_similarity
import json

class SpotifyAPI:
	def __init__(self):	
	# credential for spotify
		client_id = input("Enter your Spotify client ID:") # ***change***
		client_secret = input("Enter your Spotify client secret:")
		client_credential = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
		self.client = spotipy.Spotify(client_credentials_manager=client_credential)


	
	# serach the song track of the song from Spotify
	def search_fav_song_track(self, song_name):
		try:
			result = self.client.search(song_name, type='track')
			track_data = result["tracks"]["items"]
			return track_data
		except spotipy.client.SpotifyException as e:
			if e.http_status == 429:
				print("Rate Limit exceeded. Please wait. ")
			else:
				print("Your song is not found.")
			return None

	# get all track data of musicla songs
	def serach_musical_track(self):
		try:
			musical_results = self.client.search(q = "genre: musical", type='track')
			return musical_results["tracks"]
		except spotipy.client.SpotifyException as e:
			if e.http_status == 429:
				print("Rate Limit exceeded. Please wait. ")
			return None


class DataProcessing:
	def __init__(self, client, fav_song_results, musical_results):
		self.client = client
		self.fav_song_results = fav_song_results
		self.musical_results = musical_results
	
	# get features of the favorite song
	def get_fav_song_features(self):
		track_id = self.fav_song_results[0]["id"]
		try:
			fav_song_features = self.client.audio_features(track_id)
			features_series = pd.Series(fav_song_features) # drop "id" and remain only features
			return features_series
		except:
			return None

	
	# get a certain item list of all musical songs
	def get_musical_item_list(self, item, subitem=None):
		item_list = []
		if subitem == None:
			for track in musical_results["items"]:
				item_list.append(track[item])
		else:
			for track in musical_results["items"]:
				item_list.append(track[item][subitem])
		return item_list

	# get df of features for musical songs
	def get_musical_features(self):
		id_list = self.get_musical_item_list(self.musical_results, "id")
		try:
			musical_features = self.client.audio_features(id_list)
			features_df = pd.DataFrame(data = musical_features, columns=features[0].keys())
			features_df.set_index("id", inplace=True)
			return features_df
		except:
			return None

	# get df of infomation for musical songs
	def get_musical_info(self):
		id_list = self.get_musical_item_list(self.musical_results, "id")
		titles_list = self.get_musical_item_list(self.musical_results, "name")
		album_list = self.get_musical_item_list(self.musical_results, "album","name")
		info_df = pd.DataFrame(list(zip(titles_list, album_list)), columns=["id", "title", "album"], index=id_list)
		return info_df



class Recommend:
	def __init__(self, fav_song_feature, musical_song_features, musical_song_info):
		self.recommended_songs = None
		self.fav_song_feature = fav_song_feature
        self.musical_song_features = musical_song_features
        self.musical_song_info = musical_song_info
        self.recommended_songs = recommend_songs()
		
	# calculate similarity scores and sort based on the similarity scores
	def recommend_songs(self):
		# calculate similarity scores
		self.musical_song_info["similarity"]= cosine_similarity(self.musical_song_features, self.fav_song_features).squeeze()
		
		# sort musical songs based on the similarity scores
		self.musical_song_info_sorted_df = self.musical_song_info.sort_values(by="similarity", ascending=False) 
		return self.musical_song_info_sorted_df.reset_index(drop=True, inplace=True)
		


	# print the results
	def recommend_print(self):
		for i in range(10):
			print(f"Your No.{i} recommendation is {self.recommended_songs.iloc[i]["name"]} by {self.recommended_songs.iloc[i]["album"]}")


def main():
	client = SpotifyAPI()

	fav_song_name = input("Enter your favorite song name: ") # ask a question about favorite song and return answer
	fav_song_results = client.search_fav_song_track(fav_song_name) # get all favorite song search results 
	musical_results = client.serach_musical_track() # get all musical songs search results 

	data = DataProcessing(client, fav_song_results, musical_results)
	fav_song_features = data.get_fav_song_features() # get df of features for favorite song
	musical_song_features = data.get_musical_features() # get df of features for musical songs
	musical_song_info = data.get_musical_info() # get df of information for musical songs

	recommend = Recommendation(fav_song_features, musical_song_features, musical_song_info)
    recommend.recommend_print() # print the recommendation


if __name__ == "__main__":
	main()
