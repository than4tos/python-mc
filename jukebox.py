import sqlite3
try:
    import tkinter
except ImportError:
    import Tkinter  # python2


class Scrollbox(tkinter.Listbox):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)

        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky='nsw', rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)

        self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan)
        self['yscrollcommand'] = self.scrollbar.set


class DataListBox(Scrollbox):
    """Class to imlement Listbox with data in it"""
    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
        super().__init__(window, **kwargs)

        self.linked_box = None
        self.link_field = None
        self.artist_id = None

        self.cursor = connection.cursor()
        self.table = table
        self.field = self.table + "." + field

        self.bind('<<ListboxSelect>>', self.on_select)

        self.sql_select = "SELECT " + self.field + ", " + self.table + "._id" + " FROM " + self.table
        if sort_order:
            self.sql_sort = " ORDER BY " + ','.join(sort_order)
        else:
            self.sql_sort = " ORDER BY " + self.field

    def clear(self):
        self.delete(0, tkinter.END)

    def link(self, widget, link_field):
        self.widget = widget
        self.linked_box = widget
        widget.link_field = link_field

    def requery(self, link_value=None):
        if link_value and self.link_field:
            sql = self.sql_select + " WHERE " + self.table + "." + self.link_field + "=? " + self.sql_sort
            print("Requery: " + sql)      # TODO remove later
            self.cursor.execute(sql, (link_value,))
        else:
            print(self.sql_select + self.sql_sort)      # TODO remove later
            self.cursor.execute(self.sql_select + self.sql_sort)

        # clear list box content before re loading content
        self.clear()
        for value in self.cursor:
            self.insert(tkinter.END, value[0])

        if self.linked_box:
            self.linked_box.clear()

    def on_select(self, event):
        if self.linked_box and self.curselection():
            index = self.curselection()[0]
            value = self.get(index),

            # get the artist ID from the database row
            # sql = self.sql_select + " WHERE " + self.field + "=?"
            if self.linked_box.table == "songs":        # if select album to fetch song then execute another query
                sql = self.sql_select + " INNER JOIN artists on albums.artist = artists._id " + \
                      "WHERE " + self.field + "=? AND albums.artist=?"
                link_id = self.cursor.execute(sql, (value[0], self.artist_id)).fetchone()[1]
            else:
                sql = self.sql_select + " WHERE " + self.field + "=?"
                link_id = self.cursor.execute(sql, value).fetchone()[1]
                self.widget.artist_id = link_id

            print("Get link_id query: " + sql)      # TODO remove later

            self.linked_box.requery(link_id)
            print("Selected listbox table: {}\nSelected listbox linked table: {}"
                  "\nSelected listbox link field: {}\nSelected listbox linked link field: {}".format(
                self.table, self.linked_box.table, self.link_field, self.linked_box.link_field))     # TODO Rremove


if __name__ == "__main__":
    conn = sqlite3.connect('music.sqlite')

    mainWindow = tkinter.Tk()
    mainWindow.title('Music DB Browser')
    mainWindow.geometry('1024x768')

    # Configure row and column
    mainWindow.columnconfigure(0, weight=2)
    mainWindow.columnconfigure(1, weight=2)
    mainWindow.columnconfigure(2, weight=2)
    mainWindow.columnconfigure(3, weight=1)

    mainWindow.rowconfigure(0, weight=1)
    mainWindow.rowconfigure(1, weight=5)
    mainWindow.rowconfigure(2, weight=5)
    mainWindow.rowconfigure(3, weight=1)

    # ===== Labels =====
    tkinter.Label(mainWindow, text='Artists').grid(row=0, column=0)
    tkinter.Label(mainWindow, text='Albums').grid(row=0, column=1)
    tkinter.Label(mainWindow, text='Songs').grid(row=0, column=2)

    # ===== Artist Listbox =====
    artistList = DataListBox(mainWindow, conn, "artists", "name")
    artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
    artistList.config(border=2, relief='sunken')

    artistList.requery()

    # ===== Albums Listbox =====
    albumLV = tkinter.Variable(mainWindow)
    albumLV.set(("Choose an Artist",))
    albumList = DataListBox(mainWindow, conn, "albums", "name", sort_order=("name",))
    albumList.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
    albumList.config(border=2, relief='sunken')

    artistList.link(albumList, "artist")

    # ===== Albums Listbox =====
    songLV = tkinter.Variable(mainWindow)
    songLV.set(("Choose an Album",))
    songList = DataListBox(mainWindow, conn, "songs", "title", sort_order=("track", "title"))
    songList.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
    songList.config(border=2, relief='sunken')

    albumList.link(songList, "album")

    # mainWindow mainloop
    mainWindow.mainloop()
    conn.close()
