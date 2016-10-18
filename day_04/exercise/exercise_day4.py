#!/usr/bin/env python

"""
Python course EBC 2016
Day 4 - Exercise instructions
Lucas Sinclair <lucas.sinclair@me.com>

* Write a program in a file called "exercise_day4.py"
* You have until the start of the next course at 13h00 tomorrow to finish it.
* Once the program is done, upload it in your github repository "python_homework" in a directory named "day4".

The program should read the file named "lulu_mix_16.csv". This file should be placed in your "home" directory. Your program should use the OS environment variable "$HOME" to find the file.
This file is a comma separated values format. It contains information about different music tracks.

For each line in the file (excluding the header) the program should produce a new "Song" instance. It should place all the Song instances created in a list called "songs".

### Each Song object should have these attributes:

* title
The title of the song as a string.

* artist
The artist of the song as a string.

* duration
The title of the song as an integer in seconds.

When creating new Song instances:

-> If the duration of a song is not a number, set it to 0, but issue a warning.
-> If the duration of a song is negative, raise an Exception and stop the program.

### Each Song object should have these methods:

* pretty_duration(self)
Returns a nice string describing the duration. For instance if the duration is 3611, this methods takes no input and returns "01 hours 00 minutes 11 seconds" as a string.

* play(self)
Automatically opens a webpage on your computer with a youtube search for the title.

Once your program is ready the following four lines of code should run without errors. (After you have removed the negative duration song!).
"""

# Internal modules #
import warnings, re

# Third-party modules #
import sh

#######################################################################
class Song(object):
    """Class definition for Song objects"""

    def __init__(self, title, artist, duration):
        """Constructor"""
        self.title = title
        self.artist = artist
        try:
            duration = int(duration)
        except ValueError:
            warnings.warn('Song duration (%s) impossible to convert to a number. Sets self.duration to 0.')
            duration = 0
        if duration < 0:
            raise ValueError('Song duration cannot be negative (%s)' % duration)
        else:
            self.duration = duration
        
    
    def pretty_duration(self):
        """Returns string with song duration formatted as 'HH hours MM minutes SS seconds'"""
        t = int(self.duration)
        tdict = dict(seconds = t % 60,
            minutes = (t / 60) % 60,
            hours = t / 3600)
        tstr = ''
        for key in ['hours', 'minutes', 'seconds']:
            if tdict[key] > 0 or key == 'seconds':
                # Skip hours or minutes if zero
                tstr += '%02i %s ' % (tdict[key],key)
        return tstr.strip()
        
    def play(self):
        """Opens Firefox with a youtube search for the song"""
        youtube_str = 'https://www.youtube.com/results?search_query='
        song_str = '"%s"+"%s"' % (re.sub('[ ]+','+',self.artist), re.sub('[ ]+', '+',self.title))
        sh.firefox(youtube_str + song_str)
    
    
    

def csv2song_list(csv_file, sep = ','):
    """Parses csv_file and returns list of Song objects"""
    songs = []
    with open(csv_file, 'r') as f:
        for line in f:
            lst = line.strip().split(sep)
            if lst == ['Name','Artist','Duration'] and songs == []:
                # if line is header line
                continue
            songs.append(Song(*lst))
    return songs
            


csv_file = sh.HOME + '/lulu_mix_16.csv'
songs = csv2song_list(csv_file)

for s in songs: print s.artist
for s in songs: print s.pretty_duration()
print sum(s.duration for s in songs), "seconds in total"
songs[6].play()
