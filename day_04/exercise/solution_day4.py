# Built-in modules #
import os, sys, warnings

# Third party modules #
import sh

###############################################################################
class Song(object):
    """A class used to complete the exercise of day 4 in the
    python EBC course of year 2016."""

    def __init__(self, title, artist, duration):
        # Base parameters #
        self.title = title
        self.artist = artist
        # Attempt conversion to int #
        try:
            self.duration = int(duration)
        except ValueError:
            warnings.warn("The song '%s' had a non-number duration. It's set to zero." % self.title)
            self.duration = 0
        # Check duration is not negative #
        if self.duration < 0:
            raise Exception("You can't have a negative duration on song: " + self.title)

    def pretty_duration(self):
        secs     = self.duration
        mins     = secs / 60
        hours    = mins / 60
        return "%02i hours %02i minutes %02i seconds" % (hours, secs % 60, mins % 60)

    def play(self):
        """Idea: Use webbrowser instead to be cross-platform."""
        # Build the URL #
        base_url = "https://www.youtube.com/results?search_query="
        complete_url = base_url + self.title.replace(' ','+')
        # Depends on your operating system #
        import webbrowser
        webbrowser.open(complete_url)

###############################################################################
# Get the path to the CSV file #
home = os.environ['HOME']
input_path = home + "/lulu_mix_16.csv"

# Parse it #
handle = open(input_path, 'rb')
header_line = handle.next()
songs = [Song(*line.strip('\n').split(',')) for line in handle]

# Rado's way #
songs = []
for line in handle:
    try: s = Song(*line.strip('\n').split(','))
    except ValueError: pass
    songs.appen(s)

# The test code #
for s in songs: print s.artist
for s in songs: print s.pretty_duration()
print sum(s.duration for s in songs), "seconds in total"
songs[6].play()