import pytest
from unittest.mock import MagicMock
import pandas as pd
import spotipy

import main

song_results_expected = [
# single results
{"tracks": {"items": [
{"album":{"name": "album name"}, "id": "valid id", "name": "valid song"}
]}},
# multiple results
{"tracks": {"items": [
{"album":{"name": "album name1"}, "id": "valid id1", "name": "valid song1"},
{"album":{"name": "album name2"}, "id": "valid id2", "name": "valid song2"},
{"album":{"name": "album name3"}, "id": "valid id3", "name": "valid song3"},
]}},
]

song_features_expected = [
{
  "acousticness": 0.00242,
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/valid_id",
  "danceability": 0.585,
  "duration_ms": 237040,
  "energy": 0.842,
  "id": "valid id",
  "instrumentalness": 0.00686,
  "key": 9,
  "liveness": 0.0866,
  "loudness": -5.883,
  "mode": 0,
  "speechiness": 0.0556,
  "tempo": 118.211,
  "time_signature": 4,
  "track_href": "https://api.spotify.com/v1/tracks/valid_id",
  "type": "audio_features",
  "uri": "spotify:track:valid_id",
  "valence": 0.428
},
{
  "acousticness": 0.00242,
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/valid_id1",
  "danceability": 0.585,
  "duration_ms": 237040,
  "energy": 0.842,
  "id": "valid id1",
  "instrumentalness": 0.00686,
  "key": 9,
  "liveness": 0.0866,
  "loudness": -5.883,
  "mode": 0,
  "speechiness": 0.0556,
  "tempo": 118.211,
  "time_signature": 4,
  "track_href": "https://api.spotify.com/v1/tracks/valid_id1",
  "type": "audio_features",
  "uri": "spotify:track:valid_id1",
  "valence": 0.428
},
{
  "acousticness": 0.0024,
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/valid_id2",
  "danceability": 0.58,
  "duration_ms": 23704,
  "energy": 0.84,
  "id": "valid id2",
  "instrumentalness": 0.0068,
  "key": 8,
  "liveness": 0.086,
  "loudness": -5.88,
  "mode": 0,
  "speechiness": 0.055,
  "tempo": 118.21,
  "time_signature": 4,
  "track_href": "https://api.spotify.com/v1/tracks/valid_id2",
  "type": "audio_features",
  "uri": "spotify:track:valid_id2",
  "valence": 0.42
},
{
  "acousticness": 0.002,
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/valid_id3",
  "danceability": 0.5,
  "duration_ms": 2370,
  "energy": 0.8,
  "id": "valid id3",
  "instrumentalness": 0.006,
  "key": 7,
  "liveness": 0.08,
  "loudness": -5.8,
  "mode": 0,
  "speechiness": 0.05,
  "tempo": 118.2,
  "time_signature": 4,
  "track_href": "https://api.spotify.com/v1/tracks/valid_id3",
  "type": "audio_features",
  "uri": "spotify:track:valid_id3",
  "valence": 0.4
}]

song_features_list = [
{
  "acousticness": [0.00242, 0.0024, 0.002],
  "danceability": [0.585, 0.58, 0.5],
  "energy": [0.842, 0.84, 0.8],
  "id": ["valid_id1", "valid_id2", "valid_id3"],
  "instrumentalness": [0.00686, 0.0068, 0.006],
  "key": [9,8,7],
  "liveness": [0.0866, 0.086, 0.08],
  "loudness": [-5.883, -5.88, -5.8],
  "mode": [0,1,2],
  "speechiness": [0.0556, 0.055, 0.05],
  "tempo": [118.211, 118.21, 118.2],
  "valence": [0.428, 0.42, 0.4]
},
{
  "acousticness": [0.00242, 0.0024, 0.002].reverse(),
  "danceability": [0.585, 0.58, 0.5].reverse(),
  "energy": [0.842, 0.84, 0.8].reverse(),
  "id": ["valid_id3", "valid_id2", "valid_id1"],
  "instrumentalness": [0.00686, 0.0068, 0.006].reverse(),
  "key": [9,8,7].reverse(),
  "liveness": [0.0866, 0.086, 0.08].reverse(),
  "loudness": [-5.883, -5.88, -5.8].reverse(),
  "mode": [0,1,2].reverse(),
  "speechiness": [0.0556, 0.055, 0.05].reverse(),
  "tempo": [118.211, 118.21, 118.2].reverse(),
  "valence": [0.428, 0.42, 0.4].reverse(),
  "similarity": [0.03, 0.02, 0.01].reverse()
},
]

print("test start")
@pytest.fixture
def spotify_api():
    return SpotifyAPI()

@pytest.mark.parametrize("song_name, mock, expected",
	[
	#Test case 1: success
	(
		"Valid_song",
		song_results_expected[0],
		song_results_expected[0]["tracks"]["items"],),
	# Test case 2: error 429
	(
		"Invalide_song",
		{Exception("API error")},
		None,),
	# Test case 3: error can't find
	(
		"Invalide_song",
		{"tracks": {"items": []}},
		None,)
	])

def test_search_fav_song_track(spotify_api, song_name, mock, expected):
	spotify_api.client.search = MagicMock(return_value=mock)
	result = spotify_api.search_fav_song_track(song_name)
	assert result == expected


need_item = ["acousticness","danceability","energy","id","instrumentalness","key","liveness","loudness","mode","speechiness","tempo","valence"]
@pytest.mark.parametrize("fav_song_results, musical_results, mock, expected",
	[
	#Test case 1: success for favorite song
	(
		song_results_expected[0],
		song_results_expected[1],
		song_features_expected[0],
		pd.Series(song_features_expected[0][key] for key in need_item),
		),
	# Test case 2: error for favorite song
	(
		song_results_expected[0],
		song_results_expected[1],
		{Exception("API error")},
		None,
		),
	])

def test_get_fav_song_features(fav_song_results, musical_results, mock, expected):
	data_processing = DataProcessing(None, fav_song_results, musical_results)
	data_processing.client.audio_features = MagicMock(return_value=mock)
	result = data_processing.get_fav_song_features()
	assert result == expected

@pytest.mark.parametrize("musical_results, expected",
	[
	#Test case 1: success for favorite song
	(
		song_results_expected[1],
		["valid_id1", "valid_id2", "valid_id3"]
		),
	])
def test_get_musical_item_list(musical_results, expected):
	data_processing = DataProcessing(None, None, musical_results)
	result = data_processing.test_get_musical_item_list("id")
	assert result == expected

@pytest.mark.parametrize("mock, expected",
	[
	#Test case 1: success for musical song
	(
		song_features_expected[1:4],
		pd.DataFrame(song_features_list[0]),
		),
	# Test case 2: error for musical song
	(
		{Exception("API error")},
		None,
		),
	])

def test_get_musical_features(mock, expected):
	data_processing = DataProcessing(None, None, None)
	data_processing.get_musical_item_list = MagicMock(return_value=["valid_id1", "valid_id2", "valid_id3"])
	data_processing.client.audio_features = MagicMock(return_value=mock)
	result = data_processing.get_musical_features()
	assert result == expected

@pytest.mark.parametrize("musical_song_features, mock, expected",
	[
	#Test case 1: success 
	(
		pd.DataFrame(song_features_list[0]),
		[0.03, 0.02, 0.01],
		pd.DataFrame(song_features_list[1]),
		),
	# Test case 2: error 
	(
		pd.DataFrame(song_features_list[0]),
		[],
		None,
		),
	])
def test_recommend_song(musical_song_features, mock, expected):
	recommend = Recommend(None, musical_song_features, None)
	recommend.cosine_similarity = MagicMock(return_value=mock)
	result = recommend.recommend_song()
	assert result == expected

print("test end")
