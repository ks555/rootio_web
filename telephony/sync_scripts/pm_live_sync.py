import urllib2
import soundcloud
import time

client = soundcloud.Client(client_id='5dace0be947f5c9bb465b0fbb0b7e680')
tracks = client.get('users/wizartsmedia/tracks', limit=1)
for track in tracks:
    #print track.id
    #print track.title
    response = urllib2.urlopen('https://api.soundcloud.com/tracks/{0}/stream?client_id={1}'.format(track.id,'5dace0be947f5c9bb465b0fbb0b7e680'))
    try:
        file_name = '/home/amour/test_media/RootioNew/Northern Uganda Pilot/PM Live/{0}.mp3'.format(track.title.replace(' ', '_'))
    except Exception, e:
        file_name = '/home/amour/test_media/RootioNew/Northern Uganda Pilot/PM Live/{0}.mp3'.format(time.strftime("%c").replace(' ', '_'))
    f = open(file_name, 'w')
    f.write(response.read())
