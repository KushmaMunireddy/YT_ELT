import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env") #loads the environment variables from the .env file

API_KEY = os.getenv("API_KEY") #global variable that contains the API key for the YouTube Data API v3, loaded from an environment variable

CHANNEL_HANDLE = "MrBeast" #global variable that contains the channel handle for the YouTube channel we want to get data for

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

if __name__ == "__main__":
    
    playlist_id = get_playlist_id() #calls the get_playlist_id function and assigns the return value to the variable playlist_id
    
    print(f"Uploads Playlist ID for channel '{CHANNEL_HANDLE}': {playlist_id}") #prints the uploads playlist ID
else:
    print("This script is being imported as a module, not run directly so get_playlist_id() is not called.")
    
    
        