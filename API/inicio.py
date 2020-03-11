#!/usr/bin/env python
import datetime

import os
import getopt
import re
import sys
# flickrapi does not work with python 3
import flickrapi
import webbrowser

__author__ = 'Mike Bridge'

api_key = u'7b546b3c5860caa10ddd41448eeaf7e7'
api_secret = u'83c8e48221459d91'

flickr = flickrapi.FlickrAPI(api_key, api_secret)
print('authenticating...')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms=u'delete'):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms=u'delete')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    #verifier = unicode(raw_input('Verifier code: '))
    print(authorize_url);
    verifier = raw_input("Enter the authorization code: ");
    uverifier = unicode(verifier, "utf-8")
    print("verifier is "+uverifier)
    # Trade the request token for an access token
    flickr.get_access_token(uverifier)

print('uploading...')

class FileWithCallback(object):
    def __init__(self, filename, callback):
        self.file = open(filename, 'rb')
        self.callback = callback
        # the following attributes and methods are required
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell

    def read(self, size):
        if self.callback:
            self.callback(self.tell() * 100 // self.len)
        return self.file.read(size)

def callback(progress):
    print(".")


def upload(filename):
    print("uploading ",filename)
    params = dict()
    params['fileobj'] = FileWithCallback(filename, callback)
    rsp = flickr.upload(params)
    print(rsp)

def main(argv):
    try:
        flickr.upload(
            filename=u'1.jpg',
            title=u'Foto clase estocasticos',
            description=u'Es una foto tomada en una clase de estocasticos despues del paro.\n\n'\
                'Para mas informacion visite el grupo de estocasticos 2019 en whatsapp.\n\n'\
                'Credit: Camara de Zuly Mejia',
            is_public=u'1',
            tags=u'Clase'
        )
        print("DONE")
    except:
        print('failed upload')

if __name__ == "__main__":
   main(sys.argv[1:])