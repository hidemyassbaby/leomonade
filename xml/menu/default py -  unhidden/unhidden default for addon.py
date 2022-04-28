try:
    from resources.lib.DI import DI
    from resources.lib.plugin import run_hook, register_routes
except ImportError:
    from .resources.lib.DI import DI
    from .resources.lib.plugin import run_hook, register_routes

try:
    from resources.lib.util.common import *
except ImportError:
    from .resources.lib.util.common import *

import xbmcaddon


# root_xml_url = ownAddon.getSetting('root_xml') or "file://main.xml"

root_xml_url ="https://raw.githubusercontent.com/hidemyassbaby/leomonade/main/xml/menu/Main%20menu%20for%20addon/menu3.3.json"
#root_xml_url =  "file://scraper_list.json"
# root_xml_url =  "file://main.json"
# root_xml_url =  "file://main_pastebin_xml"
# root_xml_url =  "file://main_pastebin_json"
# root_xml_url =  "file://basics.json"
# root_xml_url =  "file://main2.xml"

plugin = DI.plugin

@plugin.route("/")
def root() -> None:
    get_list(root_xml_url)

@plugin.route("/get_list/<path:url>")
def get_list(url: str) -> None:
    do_log(f" Reading url at route >  {url}" )   
    _get_list(url)

def _get_list(url):
    do_log(f" Reading url >  {url}" )   
    response = run_hook("get_list", url)
    if response:           
        do_log(f'default - response = \n {str(response)} ' )  
        jen_list = run_hook("parse_list", url, response) 
        do_log(f'default - jen list = \n {str(jen_list)} ')  
        jen_list = [run_hook("process_item", item) for item in jen_list]
        jen_list = [
            run_hook("get_metadata", item, return_item_on_failure=True) for item in jen_list
        ]    
        run_hook("display_list", jen_list)
    else:
        run_hook("display_list", [])


@plugin.route("/play_video/<path:video>")
def play_video(video: str):
    import urllib.parse
    _play_video(video)

def _play_video(video):
    import base64
    import json
    video_link = '' 
    video = base64.urlsafe_b64decode(video)      
    if '"link":' in str(video) :
        video_link = run_hook("pre_play", video)
        if video_link : 
            run_hook("play_video", video_link)        
    else :
        run_hook("play_video", video)

@plugin.route("/settings/<path:url>")
def settings(url):
    xbmcaddon.Addon().openSettings()

register_routes(plugin)

def main():
    plugin.run()
    return 0

if __name__ == "__main__":
    main()
