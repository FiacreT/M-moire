import requests
import urllib.request
import sys
import argparse
import os
from time import sleep



def valid_story(username, singleStory=False):
    """
    Checks if the given username or id
    has a public story
    """
    if singleStory:
        url = "https://story.snapchat.com/s/s:{}"
    else:
        url = "https://story.snapchat.com/s/{}"

    url = url.format(username)
    r = requests.get(url)

    if r.status_code == 200:
        return True

    else:
        return False


def download(username, singleStory=False):

    if singleStory:
        api = "https://storysharing.snapchat.com/v1/fetch/s:{}?request_origin=ORIGIN_WEB_PLAYER"
    else:
        api = "https://storysharing.snapchat.com/v1/fetch/{}?request_origin=ORIGIN_WEB_PLAYER"

    url = api.format(username)
    response = requests.get(url)

    data = response.json()
    print("\033[92m[+] Fetched data\033[0m")

    # Using dict.get() will return None when there are no snaps instead of throwing a KeyError
    story_arr = data.get("story").get("snaps")

    if story_arr:
        story_type = data.get("story").get("metadata").get("storyType")

        title = data.get("story").get("metadata").get("title")

        # TYPE_PUBLIC_USER_STORY = Story from a user
        # There are many different story types.
        if story_type == "TYPE_PUBLIC_USER_STORY":

            username = data["story"]["id"]

            print("\33[93m[!] Downloading from",
                title, str(data["story"]["metadata"]["emoji"]),
                "(\033[91m{}\33[93m)\33[0m".format(username))
        else:
            print("\33[93m[!] Downloading from", title)

            # If dont do this the folder will be have a long
            # unidentifiable name. So we are using the title
            # as the "username"
            username = title.replace(" ", "_")
        
        # Making a directory with given username
        # to store the images of that user
        os.makedirs(username, exist_ok=True)

        for index, media in enumerate(story_arr):
            try:
                file_url = media["media"]["mediaUrl"]

                # We cant download images anymore. Its not in the JSON
                # response. But I just commented it out incase it comes
                # back.
                #if media["media"]["type"] == "IMAGE":
                    #file_ext = ".jpg"
                    #filetype = "IMAGE"

                if media["media"]["type"] == "VIDEO":
                    file_ext = ".mp4"

                    # This is name of the dir where these types
                    # of files will be stored
                    filetype = "VIDEO"

                elif media["media"]["type"] == "VIDEO_NO_SOUND":
                    file_ext = ".mp4"
                    filetype = "VIDEO_NO_SOUND"


                dir_name = username+"/"+filetype+"/"

                os.makedirs(dir_name, exist_ok=True)

                path = dir_name+str(media["id"])+file_ext

                if not os.path.exists(path):

                    urllib.request.urlretrieve(file_url, path)
                    print("\033[92m[+] Downloaded file {:d} of {:d}:\033[0m {:s}".format(index+1, len(story_arr), path.replace(dir_name, "")))
                    
                    # We need a small pause or else we will get a ConnectionResetError
                    sleep(0.3)
                
                else:
                    print("\033[91m[!] File {:d} of {:d} already exists:\033[0m {:s}".format(index+1, len(story_arr), path.replace(dir_name, "")))
            
            except KeyError as e:
                print("\033[91m[-] Could not get file data: \033[0m{:s}".format(str(e)))
            
            except KeyboardInterrupt:
                print("\033[91m[!] Download cancelled\033[0m")
                break

    else:
        print("\033[91m[!] No stories available\033[0m")


def main():
    parser = argparse.ArgumentParser(description = "A public SnapChat story downloader")
    parser.add_argument('username', action="store",
    help="The username or id of a public story")

    parser.add_argument('-s', '--single', action="store_true",
    help="Download a single story")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    elif args.single:
        if valid_story(args.username, singleStory=True):
            print("\033[92m[+] Valid story\033[0m")
            download(args.username, singleStory=True)

        else:
            print("\033[91m[-] Invalid story\033[0m")


    else:
        if valid_story(args.username):
            print("\033[92m[+] Valid story\033[0m")
            download(args.username)

        else:
            print("\033[91m[-] Invalid story\033[0m")

if __name__=="__main__":
    main()
