from django.conf import settings
from django.core.management.base import BaseCommand
import requests
import httplib2

from apps.album.models import Album
from apps.track.models import Track
from apps.user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        # user = User.objects.get(username="Idryss")
        ##print(user.email)
        ##response = requests.get("https://api.jamendo.com/v3.0/artists/albums/?client_id=bf8d52b7&format=jsonpretty&", params={'name': user.username})
        # result = response.json()["results"][0]["albums"]
        # print(result[0]["image"])
        # h = httplib2.Http('.cache')
        # resp, content = h.request(result[0]["image"])
        # out = open("media/covers/"+result[0]['name'].replace(" ", "_")+".jpg", 'wb')
        # out.write(content)
        # out.close()

        users = User.objects.all().order_by('-id')
        for user in users:
            response = requests.get(
                "https://api.jamendo.com/v3.0/albums/tracks/?client_id=bf8d52b7&format=jsonpretty&",
                params={'artist_name': user.username})
            result = response.json()["results"]
            for album in result:
                album_name = album['name']
                user_id = user.public_id
                cover = "covers/" + album['name'].replace(" ", "_") + user.username + ".jpg"
                try:
                    h = httplib2.Http('.cache')
                    resp_album, content_album = h.request(album["image"])
                    out = open("media/covers/" + album['name'].replace(" ", "_") + user.username + ".jpg", 'wb')
                    out.write(content_album)
                    out.close()
                    new_album = Album(title=album_name, author=user, cover=cover)
                    new_album.save()
                    for track in album["tracks"]:
                        try:
                            track_title = track['name'].replace(" ", "_")
                            track_music = "music/" + track_title + user.username + ".mp3"
                            resp_track, content_track = h.request(track['audio'])
                            out = open("media/music/" + track_title + user.username + ".mp3", 'wb')
                            out.write(content_track)
                            out.close()
                            new_track = Track(title=track_title, author=user, cover=cover, album=new_album,
                                              music=track_music)
                            new_track.save()
                        except Exception as e:
                            if hasattr(e, 'message'):
                                print(e.message)
                            else:
                                print(e)
                except Exception as e:
                    if hasattr(e, 'message'):
                        print(e.message)
                    else:
                        print(e)

        ##for x in range(10, 300, 10):
        ##    response = requests.get('https://api.jamendo.com/v3.0/artists/?client_id=bf8d52b7&format=jsonpretty&offset='+str(x))
        ##    result = response.json()['results']
        ##    for res in result:
        ##        try:
        ##            new_user = User(username=res['name'], email=res['name']+"@gmail.com", password="SuperPassword", avatar="avatars/person.png")
        ##            new_user.save()
        ##        except:
        ##            print('error')
