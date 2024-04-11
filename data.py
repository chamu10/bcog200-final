import pandas
import spotify
from spotipy.oauth2 import SpotifyClientCredentials
import json

class Data:
	def __init__(self):
		self.client = None # Spotify client information

		"""self.fav_song_feature = None # features of favorited song
								self.musical_song_features = None # features of musical songs
								self.musical_song_info = None # infomation of musical songs"""


		self.get_client()
		fav_song_name = self.ask_fav_song()
		self.fav_song_feature = self.get_song_features(fav_song_name)

		musical_results = serach_musical_track() # get all musical songs search results
		self.musical_song_features = self.get_musical_features(musical_results) # get df of features for musical songs
		self.musical_song_info = self.get_musical_info(musical_results) # get df of infomation for musical songs

	# credential for spotify
	def get_client(self):
		client_id = input("Enter your Spotify client ID:")
		client_secret = input("Enter your Spotify client secret:")
		client_credential = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
		self.client = spotipy.Spotify(client_credentials_manager=client_credential)

	# serach the song track of the song from Spotify
	def search_song_track(self, song_name):
		result = slef.client.search(song_name, type='track')
		track_data = result["tracks"]["items"]
		return track_data

	# get features of the song
	def get_song_features(self, song_name):
		track_id = self.search_song_track(song_name)["id"]
		features = self.client.audio_features(track_id)
		features_series = pd.Series(features[1:]) # drop "id" and remain only features
		return features

	# ask a question about favorite song and return answer
	def ask_fav_song(self):
		song_name = input("Enter your favorite song name: ")
		return song_name

	# get all track data of musicla songs
	def serach_musical_track(self):
		musical_results = slef.client.search(q = "genre: musical", type='track')
		return musical_results["tracks"]

	# get a certain item list of all musical songs
	def get_musical_item_list(self, musical_results, item, subitem=None):
		item_list = []
		if subitem == None:
			for track in musical_results["items"]:
				item_list.append(track[item])
		else:
			for track in musical_results["items"]:
				item_list.append(track[item][subitem])
		return item_list

	# get df of features for musical songs
	def get_musical_features(self, musical_results):
		id_list = self.get_musical_item_list(musical_results, "id")
		features = self.client.audio_features(id_list)
		features_df = pd.DataFrame(data = features, columns=features[0].keys())
		features_df.set_index("id", inplace=True)
		return features_df

	# get df of infomation for musical songs
	def get_musical_info(self, musical_results):
		id_list = self.get_musical_item_list(musical_results, "id")
		titles_list = self.get_musical_item_list(musical_results, "name")
		album_list = self.get_musical_item_list(musical_results, "album","name")
		info_df = pd.DataFrame(list(zip(titles_list, album_list)), columns=["id", "title", "album"], index=id_list)
		return info_df



class Recommend:
	def __init__(self):
		self.analized_df = self.analyze_songs()
		self.top_ten_df = self.recommend_songs()
		self.recommend_print()


	# return top 10 recommend musical songs
	def recommend_songs(self):
		self.analized_df = self.analized_df.sort_values(by="similarity", ascending=False) #sort musical songs based on similarity score
		self.analized_df.reset_index(drop=True, inplace=True)
		return self.analized_df

	# get df including similarity scores
	def analyze_songs(self):
		Data.musical_song_info["similarity"]= cosin_similarity(Data.musical_song_features, Data.fav_song_feature)
		return Data.musical_song_info

	# print the results
	def recommend_print(self):
		for i in range(10):
			print(f"Your No.{i} recommendation is {self.top_ten_df[i]["name"]} by {self.top_ten_df[i]["album"]}")


def main():
	Data()
	Recommend()

if __name__ == "__main__":
	main()
