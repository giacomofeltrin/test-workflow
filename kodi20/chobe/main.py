import os
import sys
from urllib.parse import urlencode, parse_qsl, quote

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath

from animeita import get_animesaturn_filter, get_animesaturn_search, get_animesaturn_episodes, get_actual_anime_url

# Get the plugin url in plugin:// notation.
URL = sys.argv[0]
# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])
# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
ICONS_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'icons')
FANART_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'fanart')

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(URL, urlencode(kwargs))

def get_user_input():  
    kb = xbmc.Keyboard('', 'Please enter the video title')
    kb.doModal() # Onscreen keyboard appears
    if not kb.isConfirmed():
        return
    query = kb.getText() # User input
    return query

"""
Two styles of play video
def play_video(path):
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)

def play_video(path):
    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(path)
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)
"""

def play_avideo(episode_url):
    path = get_actual_anime_url(episode_url)
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)

def get_aepisodes(urlscheda):
    videos = get_animesaturn_episodes(urlscheda)
    return videos

def list_aepisodes(urlscheda):
    # Get the list of videos in the search.
    videos = get_aepisodes(urlscheda)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['title'])
        # Set additional info for the list item.
        list_item.setInfo('url', {'title': video['title'], 'episode_number': video['episode_number']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = get_url(action='aplay', video=video['url'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)

def get_avideos(abutton):
    if abutton == "Recently Added":
        videos = get_animesaturn_filter('filter?years%5B0%5D=2023')
        return videos
    elif abutton == "Search":
        query = get_user_input() # User input via onscreen keyboard
        if not query:
            return [] # Return empty list if query is blank
        subpath = "animelist?search={}".format(quote(query))
        videos = get_animesaturn_search(subpath)
        return videos

def list_avideos(abutton):
    # Get the list of videos in the search.
    videos = get_avideos(abutton)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['title'])
        # Set additional info for the list item.
        list_item.setInfo('url', {'title': video['title'], 'year': video['year'], 'plot': video['plot']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'poster': video['poster'], 'icon': video['poster'], 'fanart': video['poster']})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        url = get_url(action='getaepisodes', video=video['url'])
        # Add the list item to a virtual Kodi folder.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)

ABUTTONS = ["Recently Added", "Search"]

def get_abuttons():
    return ABUTTONS

def list_animeita():
    abuttons = get_abuttons()
    # Iterate through categories
    for abutton in abuttons:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=abutton)
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': abutton, 'genre': abutton})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='abutton', abutton=abutton)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)

CATEGORIES = [
    {
        'category': 'AnimeITA',
        'icon': None,
        'fanart': None,
        'main_menu': 'list_animeita'
    },
    {
        'category': 'Serie',
        'icon': None,
        'fanart': None,
        'main_menu': 'list_serie'
    }
]

def get_categories():
    return CATEGORIES

def list_categories():
    categories = get_categories()
    for index, category_info in enumerate(categories):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=category_info['category'])
        # Set images for the list item.
        list_item.setArt({'icon': category_info['icon'], 'fanart': category_info['fanart']})
        # Create a URL for a plugin recursive call.
        url = get_url(action='opencategory', category_menu=category_info['main_menu'])
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if not params:
        list_categories()
    elif params['action'] == 'opencategory':
        if params['category_menu'] == 'list_animeita':
            list_animeita()
        else: 
            list_animeita()
    elif params['action'] == 'abutton':
        list_avideos(params['abutton'])
    elif params['action'] == 'getaepisodes':
        list_aepisodes(params['video'])
    elif params['action'] == 'aplay':
        play_avideo(params['video'])
    else:
        raise ValueError(f'Invalid paramstring: {paramstring}!')

if __name__ == '__main__':
    router(sys.argv[2][1:])