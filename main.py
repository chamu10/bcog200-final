import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.metrics.pairwise import cosine_similarity
import json

class SpotifyAPI:
	def __init__(self):	
	# credential for spotify
		client_id = os.environ.get('client_id') 
		client_secret = os.environ.get('client_secret')
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
	
	need_item = ["acousticness","danceability","energy","id","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","valence"]

	# get features of the favorite song
	def get_fav_song_features(self):
		track_id = self.fav_song_results[0]["id"]
		try:
			fav_song_features = self.client.audio_features(track_id)
			fav_song_features = [fav_song_features[key]for key in need_item]
			features_series = pd.Series(fav_song_features) 
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
			musical_features_list = []
			for track_id in id_list:
				musical_features = self.client.audio_features(track_id)
				musical_features = [musical_features[key]for key in need_item]
				musical_features_list.append(musical_features)

			features_df = pd.DataFrame(data = musical_features_list, columns=musical_features_list[0].keys())
			#features_df.set_index("id", inplace=True)
			return features_df
		except:
			return None

	"""# get df of infomation for musical songs
				def get_musical_info(self):
					id_list = self.get_musical_item_list(self.musical_results, "id")
					titles_list = self.get_musical_item_list(self.musical_results, "name")
					album_list = self.get_musical_item_list(self.musical_results, "album","name")
					info_df = pd.DataFrame(list(zip(titles_list, album_list)), columns=["id", "title", "album"], index=id_list)
					return info_df"""



class Recommend:
	def __init__(self, fav_song_feature, musical_song_features, musical_results):
		self.recommended_songs = None
		self.fav_song_feature = fav_song_feature
		self.musical_song_features = musical_song_features
		self.musical_results = musical_results
		self.recommended_songs = recommend_songs()
        
	# calculate similarity scores and sort based on the similarity scores
	def recommend_songs(self):
		# calculate similarity scores
		self.musical_song_features["similarity"]= cosine_similarity(self.musical_song_features, self.fav_song_features).squeeze()
		
		# sort musical songs based on the similarity scores
		return self.musical_song_features.sort_values(by="similarity", ascending=False).reset_index(drop=True, inplace=True) 
		

	# print the results
	def recommend_print(self):
		for i in range(3):
			target_id = self.recommended_songs[i]["id"]
			target_track = self.musical_results["items"][self.musical_results["items"]["id"]==target_id]
			print(f"Your No.{i} recommendation is {target_track["name"]} by {target_track["album"]["name"]}")


def main():
	client = SpotifyAPI()

	fav_song_name = input("Enter your favorite song name: ") # ask a question about favorite song and return answer
	fav_song_results = client.search_fav_song_track(fav_song_name) # get all favorite song search results 
	musical_results = client.serach_musical_track() # get all musical songs search results 

	data = DataProcessing(client, fav_song_results, musical_results)
	fav_song_features = data.get_fav_song_features() # get df of features for favorite song
	musical_song_features = data.get_musical_features() # get df of features for musical songs
	#musical_song_info = data.get_musical_info() # get df of information for musical songs

	recommend = Recommendation(fav_song_features, musical_song_features, musical_song_results)
	recommend.recommend_print() # print the recommendation


if __name__ == "__main__":
	main()
