import os
import os.path as path
import hashlib
import urllib2
import re
from config import TMPDIR, EXTENSIONS, BANWORDS


class FileTools(object):
    @staticmethod
    def hash_file(file_path):
        """ Returns the short and long ed2k hash of a given file. """
        md4 = hashlib.new('md4').copy

        def gen(f):
            while True:
                x = f.read(9728000)
                if x:
                    yield x
                else:
                    return

        def md4_hash(data):
            m = md4()
            m.update(data)
            return m

        with open(file_path, 'rb') as f:
            a = gen(f)
            hashes = [md4_hash(data).digest() for data in a]
            if len(hashes) == 1:
                md4 = hashes[0].encode("hex")
            else:
                md4 = md4_hash(reduce(lambda a, d: a + d, hashes,\
                                       "")).hexdigest()
        return str(md4), 'ed2k://|file|' + path.split(file_path)[1] + '|'\
            + str(path.getsize(file_path)) + '|' + str(md4) + '|'

    @staticmethod
    def download_image(url):
        """Fetch image at url and copy it in the
        application temporary directory.
        Returns the path to the local image or empty
        string if not found."""
        if url != "":
            fname = TMPDIR + os.path.basename(url)
            response = urllib2.urlopen(url)
            with open(fname, 'w') as f:
                f.write(response.read())
            ed2hash = FileTools.hash_file(fname)[0]
            ext = os.path.splitext(fname)[1]
            newfname = TMPDIR + ed2hash
            if len(ext) > 0:
                newfname += ext
            os.rename(fname, newfname)
            return newfname
        return ""

    @staticmethod
    def recurse_files(ifiles):
        """Get recursively all media files of a directory and
        its subdirectories. Media files are recognized
        thanks to their extension."""
        files = []
        for f in ifiles:
            if path.isdir(f):
                try:
                    subs = os.listdir(f)
                except OSError:
                    break
                new_files = []
                for a in zip([f] * len(subs), subs):
                    new_files.append(path.join(a[0], a[1]))
                files += FileTools.recurse_files(new_files)
            else:
                if f.split(".")[-1].lower() in EXTENSIONS:
                    files.append(f)
        return files

    @staticmethod
    def preprocess_query(moviename):
        """Heuristic used to clean a movie title.
        Removing tags, sub informations, etc."""
        moviename = re.sub("[\.\-\_\~@]", " ", moviename)
        moviename = re.sub("[ ]+", " ", moviename)
        moviename = re.sub("[\&]", "and", moviename)
        moviename = moviename.lower()

        # Team tag removing
        motif = "[\[\(\{\<][^\]\)\}\>]+[\]\)\}\>]"
        moviename = re.sub(motif, "", moviename)

        # Continue until a stopword is found.
        tmp = re.findall("[^\(\[\{\<]+", moviename)
        if len(tmp) > 0:
            moviename = tmp[0]

        tmp = (moviename.strip()).split(" ")
        moviename = []
        for word in tmp:
            if word in BANWORDS:
                break
            moviename.append(word)
        return moviename

    @staticmethod
    def rename(movie):
        """Rename a movie based on its current title"""
        dirname = os.path.dirname(movie.get_filename())
        ext = os.path.splitext(os.path.basename(movie.get_filename()))[1]
        ext = ext.lower()
        newfilename = "%s/%s%s"%(dirname, movie.to_string(), ext)

        print "Current file : %s"%(movie.get_filename())
        print "Rename       : %s"%(newfilename)

        movie.set_filename(newfilename)
