import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.metrics.pairwise import cosine_similarity
import json

class SpotifyAPI:
	def __init__(self):	
		self.client = self.spotify_credential()
	

	# credential for spotify
	def spotify_credential(self):
		client_id = os.environ.get('CLIENT_ID') 
		client_secret = os.environ.get('CLIENT_SECRET')
		client_credential = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
		client = spotipy.Spotify(client_credentials_manager=client_credential)
		return client


	
	# serach the song track of the song from Spotify
	def search_fav_song_track(self, song_name):
		try:
			result = self.client.search(song_name, type='track')
			track_data = list(result["tracks"]["items"]) #convert set to list
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
			musical_results = self.client.search(q = "Top 100 Musical Songs", type='track', limit=50)
			musical_track = list(musical_results["tracks"]["items"]) #convert set to list
			return musical_track
		except spotipy.client.SpotifyException as e:
			if e.http_status == 429:
				print("Rate Limit exceeded. Please wait. ")
			return None


class DataProcessing:
	def __init__(self, client, fav_song_results, musical_results):
		self.client = client
		self.fav_song_results = fav_song_results
		self.musical_results = musical_results
		self.need_item = ["acousticness","danceability","energy","id","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","valence"]

	# get features of the favorite song
	def get_fav_song_features(self):
		track_id = self.fav_song_results[0]["id"]
		try:
			fav_song_features = self.client.audio_features(track_id) 
			features_series = pd.Series({key: fav_song_features[0][key] for key in self.need_item})
			return features_series.drop("id")
		except:
			return None

	
	# get a certain item list of all musical songs
	def get_musical_item_list(self, item, subitem=None):
		item_list = []
		if subitem == None:
			for track in self.musical_results:
					item_list.append(track[item])
		else:
			for track in self.musical_results:
				item_list.append(track[item][subitem])
		return item_list

	# get df of features for musical songs
	def get_musical_features(self):
		id_list = self.get_musical_item_list("id")
		try:
			musical_features_list = []
			for track_id in id_list:
				musical_features = self.client.audio_features(track_id)
				musical_features = [musical_features[0][key]for key in self.need_item]
				musical_features_list.append(musical_features)
			
			features_df = pd.DataFrame(data = musical_features_list, columns=self.need_item)
			features_df.set_index("id", inplace=True) 
			return features_df
		except:
			return None

	# get df of infomation for musical songs
	def get_musical_info(self):
		id_list = self.get_musical_item_list("id")
		titles_list = self.get_musical_item_list("name")
		album_list = self.get_musical_item_list("album","name")
		info_df = pd.DataFrame([id_list, titles_list, album_list], index=["id", "title", "album"]).T
		return info_df



class Recommend:
	def __init__(self, fav_song_features, musical_song_features, musical_results, musical_song_info):
		self.recommended_songs = None
		self.fav_song_features = fav_song_features
		self.musical_song_features = musical_song_features
		self.musical_results = musical_results
		self.musical_song_info = musical_song_info
		
        
	# calculate similarity scores and sort based on the similarity scores
	def recommend_songs(self):
		# calculate similarity scores
		fav_song_features_2D = pd.DataFrame(self.fav_song_features).transpose()
		self.musical_song_features["similarity"]= cosine_similarity(self.musical_song_features, fav_song_features_2D).squeeze()
		# sort musical songs based on the similarity scores
		return self.musical_song_features.sort_values(by="similarity", ascending=False) 
		

	# print the results
	def recommend_print(self, recommended_songs):
		for i in range(3):
			target_id = recommended_songs.index[i]
			target_track = self.musical_song_info[self.musical_song_info["id"]==target_id]
			print("Your No {} recommendation is {} from the album '{}'".format(i+1, target_track["title"].to_string(index=False), target_track["album"].to_string(index=False)))


def main():
	api = SpotifyAPI()
	client = api.spotify_credential()
	fav_song_name = input("Enter your favorite song name: ") # ask a question about favorite song and return answer
	fav_song_results = api.search_fav_song_track(fav_song_name) # get all favorite song search results 
	musical_results = api.serach_musical_track() # get all musical songs search results 

	data = DataProcessing(client, fav_song_results, musical_results)
	fav_song_features = data.get_fav_song_features() # get df of features for favorite song
	musical_song_features = data.get_musical_features() # get df of features for musical songs
	musical_song_info = data.get_musical_info() # get df of information for musical songs
	

	recommend = Recommend(fav_song_features, musical_song_features, musical_results, musical_song_info)
	recommended_songs = recommend.recommend_songs() # calculate similarity scores and sort based on the similarity scores
	recommend.recommend_print(recommended_songs) # print the recommendation


if __name__ == "__main__":
	main()
