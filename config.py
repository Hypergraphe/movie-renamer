TMPDIR = '/tmp/movie-renamer/'
WORDSLIMIT = 4
NUMRES = 3
OS = False
MAXRETRY = 3
SOCKETTIMEOUT = 5
SLEEP = 0

BANWORDS = ["dvdrip", "subtitle", "vostfr", "vost", "french", "truefrench"]
EXTENSIONS = ["avi", "mkv", "mp4", "mpeg4", "mpg", "mpeg", "divx",
            "x264", "iso", "ogv", "flv", "rv", "wmv", "264", "gvi",
            "mov", "mpg2", "ogx", "xvid"]
HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux i686; rv:10.0.7) Gecko/20100101\
     Firefox/10.0.7 Iceweasel/10.0.7",
    'Accept': 'text/html,application/xhtml+xml,application/xml;\
    q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Charset': 'utf-8;q=0.7,*;q=0.7',
    'Connection': 'Keep-Alive',
    'Cookie': 'country_code=FR'
    }
