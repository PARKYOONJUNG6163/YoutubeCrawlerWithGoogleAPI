
# coding: utf-8

# In[21]:


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

import pandas as pd
import json


# In[22]:


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBT7s07LWChD3MdGmItBegj21q0Wh7-jOs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# In[23]:


def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=q,
        type="video",
        pageToken=token,
        order = order,
        part="id,snippet",
        maxResults=max_results,
        location=location,
        locationRadius=location_radius
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return(nexttok, videos)
    except Exception as e:
        nexttok = "last_page"
        return(nexttok, videos)


# In[24]:


def geo_query(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails, statistics'

    ).execute()

    return video_response


# In[50]:


def grab_videos(keyword, token=None):
    res = youtube_search(keyword, token=token)
    token = res[0]
    videos = res[1]
    
    for vid in videos:
        total_list.append([vid['snippet']['title'],vid['snippet']['publishedAt']])

    return token


# In[51]:


youtube_search("python")

total_list = []
token = grab_videos("python")
while token != "last_page":
    token = grab_videos("python", token=token)

print(total_list)

