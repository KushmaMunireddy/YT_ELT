import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env") #loads the environment variables from the .env file

API_KEY = os.getenv("API_KEY") #global variable that contains the API key for the YouTube Data API v3, loaded from an environment variable

CHANNEL_HANDLE = "MrBeast" #global variable that contains the channel handle for the YouTube channel we want to get data for

maxResults = 50 #global variable that contains the maximum number of results to return per page when calling the YouTube Data API v3

def get_playlist_id():
    try :

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}" #url is the endpoint of the API that we are going to call

        response= requests.get(url) # response is a response object that contains the response from the API
        # print(response)
        response.raise_for_status()  # Raises an HTTPError if the response status code indicates an error (4xx or 5xx)

        data = response.json()# data is a python object (dictionary) that contains the response from the API in JSON format
        # print(data)

        # print(json.dumps(data, indent=4))  #converts python object into json string and indents it for better readability

        channel_items = data["items"][0]

        channel_playlistID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"] #accesses the uploads playlist ID from the response data  
        # print(channel_playlistID) #prints the uploads playlist ID
        
        return channel_playlistID #returns the uploads playlist ID
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except KeyError as e:
        print(f"Key error: {e}. The expected key was not found in the response data.")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}. The response data could not be decoded as JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_playlist_items(playlist_id):
    
    video_ids = [] #video_ids is a list that will contain the video IDs of the videos in the playlist
    page_token = None #page_token is a variable that will contain the next page token for pagination
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}" #base_url is the endpoint of the API that we are going to call to get the playlist items
        
    try:
        
        while True:
            url = base_url
            if page_token:
                url += f"&pageToken={page_token}" #adds the page token to the url if it exists

            response = requests.get(url) #response is a response object that contains the response from the API
            response.raise_for_status()  # Raises an HTTPError if the response status code indicates an error (4xx or 5xx)

            data = response.json() #data is a python object (dictionary) that contains the response from the API in JSON format

            for item in data.get("items", []): #iterates through the items in the response data
                video_id = item["contentDetails"]["videoId"] #accesses the video ID from the response data
                video_ids.append(video_id) #appends the video ID to the list of video IDs

            page_token = data.get("nextPageToken") #gets the next page token from the response data
            if not page_token: #if there is no next page token, break out of the loop
                break

        return video_ids #returns the list of video IDs
    except Exception as e:
        print(f"An unexpected error occurred while constructing the URL: {e}")


if __name__ == "__main__":
    
    playlist_id = get_playlist_id() #calls the get_playlist_id function and assigns the return value to the variable playlist_id
    video_ids = get_playlist_items(playlist_id) #calls the get_playlist_items function and passes the playlist_id as an argument
    print(f"Video IDs in playlist '{playlist_id}': {video_ids}")
