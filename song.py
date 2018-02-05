class Song:
    """ Song class to define song attributes

    Attributes:
        title(str) = title of the song
        artist(Artist) = artist object representing object creator
        duration(int) = a duration of song in a second, might be zero
    """

    def __init__(self, title, artist, duration=0):
        """ init function for song class

        Args:
            title (str) = initialize title attribute,
            artiest (Artist) = an artiest object representing object creator
            duration (int) = default 0 if not specified, 
                initialize duration attribute
        """
        self.title = title
        self.artist = artist
        self.duration = duration

class Album:
    """ Album class to define album attribute

    Attributes:
        name (str): name of the album
        year (int): year of the album released
        artist (Artist): artist object of an album. if none specified
            default to "Various Artist"
        track (list[song]): a list of the song in the album

    method:
        add_song: add song to the album track list
    """
    def __init__(self, name, year, artist=None):
        self.name = name
        self.year = year
        if self.artist is None:
            self.artist = Artist("Various Artist")
        else:
            self.artist = artist
        self.track = []

    def add_song(self, song, position=None):
        """ Method to add song

        Args:
            song (Song): add song object to album
            position (optional(int)): if specified define a position of the
                song in the album track list, insert between other song if
                necessary, otherwise add to end of the list
        """
        if position is None:
            self.track.append(song)
        else:
            self.track.insert(position, song)

class Artist:
    """ Artist class to store artist detail

    Attributes:
        name (str): name of the artist
        albums (list[Album]): a list containing album related to the artist.
            the list include album in this collection and not an exhaustive list 
            of artist's published album

    method:
        add_album: add album to album list attributes
    """
    def __init__(self, name):
        self.name = name
        self.albums = []
    
    def add_album(self, album):
        """ method to add album related to artist to album list

        Args:
            album (Album): Album object to add to the list
                if the album already present it will not add again (not yet implemented)
        """
        self.albums.append(album)
