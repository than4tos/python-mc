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
        if artist is None:
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


def load_data():
    new_artist = None
    new_album = None
    artist_list = []

    with open("C:\\Users\\ario.bramasto\\Documents\\Temp\\Playground\\Section-12\\albums.txt", "r") as albums:
        for line in albums:
            # data consist of (artist, album, year, song)
            artist_field, album_field, year_field, song_field = tuple(line.strip("\n").split("\t"))
            year_field = int(year_field)
            print("{}:{}:{}:{}".format(artist_field, album_field, year_field, song_field))

            if new_artist is None:
                new_artist = Artist(artist_field)
            elif new_artist.name != artist_field:
                # we've just read details for new artist
                # store current album in current artist collection then create new artist object
                new_artist.add_album(new_album)
                artist_list.append(new_artist)
                new_artist = Artist(artist_field)
                new_album = None

            if new_album is None:
                new_album = Album(album_field, year_field, new_artist)
            elif new_album.name != album_field:
                # we've just read new album for current artist
                # store current album in the artist's collection then create new album object
                new_artist.add_album(new_album)
                new_album = Album(album_field, year_field, new_artist)

            # create new song object and add it to current album collection
            new_song = Song(song_field, new_artist)
            new_album.add_song(new_song)

        # after reach the end of text file, add artist that haven't
        # been stored - process them now
        if new_artist is not None:
            if new_album is not None:
                new_artist.add_album(new_album)
            artist_list.append(new_artist)

    return artist_list


def create_checkfile(artist_list):
    """create check file from object data as comparison with original file"""
    with open("C:\\Users\\ario.bramasto\\Documents\\Temp\\Playground\\Section-12\\checkfile.txt", "w") as checkfile:
        for new_artist in artist_list:
            for new_album in new_artist.albums:
                for new_song in new_album.track:
                    print("{0.name}\t{1.name}\t{1.year}\t{2.title}".format(new_artist, new_album, new_song),
                        file=checkfile)


if __name__ == '__main__':
    artists = load_data()
    create_checkfile(artists)