#!/usr/bin/python
#-*- Coding: utf-8 -*-

#    The file is part of the Movie Renamer Collection, a simple
#    python tool to rename and export you Media Library.
#
#    Copyright (C) 2011  Hypergraphe
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import abc
import sys
import re
import os
import httplib
import htmlentitydefs
import json
from tools.BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from tools.observerdp import Observable
import urlparse
from tools.FileTools import FileTools
from config import MAXRETRY, SOCKETTIMEOUT, WORDSLIMIT, HEADERS, NUMRES


def retry_on_timeout(func):
    """HTTPConnection Timeout Decorator"""
    def wrapper(*args, **kwargs):
        retry = 0
        while(retry <= MAXRETRY):
            try:
                kwargs["timeouted"] = True
                return func(*args, **kwargs)
            except Exception:
                print >> sys.stderr, 'Connection timed out. Retrying ...'
                retry += 1
    return wrapper


# TODO Model + listeners
class MovieCollectionModel(Observable):
    def __init__(self):
        ## The model is a dict where keys are the filename
        super(MovieCollectionModel, self).__init__()
        self._movies = []
        self._candidates = {}

    def add_movie(self, movie):
        if movie in self._movies:
            return
        self._movies.append(movie)
        self.set_changed()
        self.notify_all(("add", movie))

    def remove_movie(self, movie):
        if movie in self._movies:
            self.set_changed()
            self.notify_all(("remove", movie))
            self._movies.remove(movie)

    def clear(self):
        self.set_changed()
        self.notify_all(("clear", None))
        self._movies = []

    def data(self):
        return self._movies

    def get_candidates(self, movie):
        if movie in self._candidates:
            return self._candidates[movie]
        else:
            return []

    def set_candidates(self, movie, candidates):
        """Set candidates for a movie"""
        self._candidates[movie] = candidates

    def affect_candidate(self, movie, candidate):
        """Updates the movie with candidate informations"""
        movie.update(candidate)
        self.set_changed()
        self.notify_all(("update", movie))

    def save_movie(self, movie):
        movie.set_saved()
        movie.set_modified(False)
        FileTools.rename(movie)
        self.set_changed()
        self.notify_all(("update", movie))

    def reset_movie_informations(self, movie):
        movie.reset()
        self.save_movie(movie)
        self.set_changed()
        self.notify_all(("clear", movie))


class GoogleImdbResultCandidate(object):
    """A candidate of a Google query on Imdb for a movie name"""
    def __init__(self, movie_name=u"", imdb_link=u"",
                 description=u"", cover=u"", year=""):
        self._title = movie_name.strip()
        self._imdb_link = imdb_link
        self._description = description
        self._cover = cover
        if cover != u"":
            url = urlparse.urlparse(cover)
            if url.scheme == "http":
                self._cover = FileTools.download_image(cover)
        self._year = year

    def get_cover(self):
        return self._cover

    def get_title(self):
        """Accessor to get the movie title"""
        return self._title

    def get_imdb_link(self):
        """Accessor to get the movie imdb link"""
        return self._imdb_link

    def get_year(self):
        return self._year

    def get_desc(self):
        """Accessor to get a movie description like director and major
        actors"""
        return self._description

    def to_string(self):
        if self.get_year() == "":
            return self.get_title()
        return u"%s (%s)"%(self.get_title(), self.get_year())

    def __repr__(self):
        return u"%s | %s | %s"%(self._title, self._year, self._imdb_link)


class Movie(GoogleImdbResultCandidate):
    """A representation of a Movie file in the Model. This class wraps a movie file on the
    filesystem."""
    def __init__(self, filename, movie_name=u"", imdb_link=u"", 
                 description=u""):
        super(Movie, self).__init__(movie_name, imdb_link, description)
        self._filename = unicode(filename)
        if movie_name == u"":
            ext = self.file_extension()
            if len(ext) != 0:
                self._title = self.file_basename()[:-len(ext) - 1].strip()
            else:
                self._title = self.file_basename().strip()
        self._movie_basename = self._title
        self._save = False
        self._modified = False

    def has_changed(self):
        return self._modified

    def set_modified(self, state):
        self._modified = state

    def get_filename(self):
        """Accessor to get the movie filename on disk"""
        return self._filename

    def set_filename(self, name):
        self._filename = name

    def movie_basename(self):
        return self._movie_basename

    def file_basename(self):
        """Get file basename."""
        return os.path.basename(self._filename)

    def file_dirname(self):
        """Get file path name"""
        return os.path.dirname(self._filename)

    def file_extension(self):
        """Get file extension"""
        basename = self.file_basename()
        chunks = basename.split(".")
        if len(chunks) > 1:
            return chunks[-1]
        return ""

    def get_title(self):
        """Get the movie basename without the extension"""
        return self._title

    def update(self, proposition):
        self._title = proposition.get_title()
        self._imdb_link = proposition.get_imdb_link()
        self._description = proposition.get_desc()
        self._cover = proposition.get_cover()
        self._year = proposition.get_year()
        self._modified = True

    def reset(self):
        self._title = os.path.splitext(self.movie_basename())[0]
        self._description = u""
        self._cover = u""
        self._imdb_link = u""
        self._year = u""
        self._modified = False

    def has_been_saved(self):
        return self._save

    def set_saved(self, val=True):
        self._save = val

    def __repr__(self):
        return super(Movie, self).__repr__()

    def __eq__(self, movie):
        return movie.get_filename() == self.get_filename()


class QueryEngine(object):
    def __init__(self):
        self._api_url = ""
        self._api_port = "80"

    @abc.abstractmethod
    def query(self, words, disjunction=False):
        return

    @abc.abstractmethod
    def extract_results(self, results):
        return

    @retry_on_timeout
    def request(self, method, url, body=None, headers={}, timeouted=False,
                server=""):
        if server == '':
            server = self._api_url

        if self._connection == None:
            self._connection = httplib.HTTPConnection(server,
                                                      port=self._api_port,
                                                      timeout=SOCKETTIMEOUT)
        if timeouted:
            self._connection.close()
            self._connection = httplib.HTTPConnection(server,
                                                      port=self._api_port,
                                                      timeout=SOCKETTIMEOUT)

        self._connection.request(method, url, body, headers)
        response = self._connection.getresponse()
        results = response.read()
        return results


class GoogleQuery(QueryEngine):
    def __init__(self, words_limit=WORDSLIMIT):
        """words_limit: limits the query list to a certain number of terms"""
        self._words_limit = words_limit
        self._connection = None
        self._api_url = "www.google.fr"
        self._api_port = "80"

    def query(self, words, disjunction=False):
        """Query Google with the template "site:www.imdb.com movie name"
        and returns the html answer."""
        if(len(words) > self._words_limit):
            words = words[0:self._words_limit - 1]
        qargs = ''.join([x + "+" for x in words])[:-1]
        if disjunction:
            query = "/search?as_oq=%s&as_sitesearch=www.imdb.com"%(qargs)
        else:
            query = "/search?q=site:www.imdb.com+%s"%(qargs)

        query = query.encode("utf-8")
        headers = {
            'Host': "www.google.com",
            'Referer': "http://www.google.com/",
            'Accept-Charset': "utf-8"
            }
        headers.update(HEADERS)
        r = self.request("GET", query, headers=headers)
        r = unicode(r, "utf-8", 'replace')
        return r

    def extract_results(self, results):
        """Takes a Google result html page and extract informations.
        The information is a list of GoogleImdbResultCandidate."""
        google_soup = BeautifulSoup(results, \
                    convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        res = google_soup.findAll(u"li")
        data = []
        number = 0
        for item in res:
            if hasattr(item, u"class"):
                if item.get(u"class") == u"g":
                    if number >= NUMRES:
                        break
                    number += 1
                    title = u"".join(map((lambda x: \
                            re.sub(u"<[^>]+>", "", unicode(x))),
                                         item.h3.a.contents))
                    attempt = re.findall(u"([^\-]*?) \-", title)
                    if len(attempt) > 0:
                        title = attempt[0]
                    title = title.strip()

                    regmatch = re.findall("\(([\d]+)\)", title)
                    year = u""
                    if len(regmatch) > 0:
                        year = unicode(regmatch[0])
                    title = re.sub("\([\d]+\)", "", title)

                    details = u"Year : %s\n"%year
                    details += u' '.join(item.find("span",\
                                 {"class": "st"}).findAll(text=True))

                    cover = self.google_image(title)
                    result = GoogleImdbResultCandidate(title,
                                                       item.h3.a["href"],
                                                       details,
                                                       cover,
                                                       year)
                    data.append(result)
        return data

    def google_image(self, query):
        """Fetch the first image of a Google image query"""
        additionnalkw = "+dvd+movie+cover"
        query = "+".join(query.split(" ")) + additionnalkw
        query = "/ajax/services/search/images?q=%s&v=1.0&imgsz=medium"%(query)
        query = query.encode("utf-8")
        headers = {
            'Host': "ajax.googleapis.com",
            'Accept-Charset': "utf-8"
            }
        headers.update(HEADERS)

        r = self.request("GET",
                         query,
                         headers=headers,
                         server="ajax.googleapis.com")
        try:
            r = json.loads(r, "utf-8")
            if 'responseData' in r:
                response = r['responseData']
                if 'results' in response:
                    results = response['results']
                    if len(results) > 0:
                        first = results[0]
                        if 'url' in first:
                                return FileTools.download_image(first['url'])
        except Exception as e:
            print >> sys.stderr, "Error while fetching cover : %s."%(e)

        return ""


class AllocineQuery(QueryEngine):
    def __init__(self, words_limit=WORDSLIMIT):
        self._words_limit = words_limit
        self._api_url = "api.allocine.fr"
        self._api_port = "80"
        self._query_parameters = {
                                  "partner": "yW5kcm9pZC12M3M",
                                  "page": "1",
                                  "count": "25",
                                  "filter": "movie,theater",
                                  "profile": "large",
                                  "format": "json"}
        self._connection = None

    def query(self, words, disjunction=False):
        if(len(words) > self._words_limit):
            words = words[0:self._words_limit - 1]
        qargs = ''.join([x + "%20" for x in words])[:-3]

        parameters = "&".join(["%s=%s"%(k,v) for (k,v) \
                      in self._query_parameters.items()])
        query = "/rest/v3/search?%s&q=%s"%(parameters, qargs)
        query = query.encode("utf-8")

        headers = {
            'Host': "api.allocine.fr",
            'Accept-Charset': "utf-8"
        }
        headers.update(HEADERS)
        result = self.request("GET", query, headers=headers)
        result = unicode(result, "utf-8", 'replace')
        dump_result = json.loads(result)

        results = {}

        if 'feed' in dump_result:
            if 'totalResults' in dump_result['feed']:
                if dump_result['feed']['totalResults'] > 0:
                    results = dump_result['feed']['movie']
        return results

    def extract_results(self, results):
        headers = {
            'Host': "api.allocine.fr",
            'Accept-Charset': "utf-8"
        }
        headers.update(HEADERS)
        data = []
        results = results[:NUMRES] if len(results) >= NUMRES else results
        for movie in results:
            if 'code' in movie:
                parameters = "partner=%s&format=%s"%(
                                self._query_parameters["partner"],
                                self._query_parameters["format"])
                query = "/rest/v3/movie?%s&code=%s"%(parameters, movie["code"])
                result = self.request("GET", query, headers=headers)
                result = unicode(result, "utf-8", 'replace')
                dump_result = json.loads(result)
                entry = dump_result["movie"]

                description = u""
                if u'originalTitle' in entry:
                    description += u"Original Title : %s\n"%(entry[u'originalTitle'])

                title = u""
                if u'title' in entry:
                    title = entry[u'title']
                    description += u"Title : %s\n"%(entry[u'title'])

                year = u""
                if u'productionYear' in entry:
                    year = entry[u'productionYear']
                    description += "Year : %s\n"%(entry[u'productionYear'])

                if u'castingShort' in entry:
                    casting = entry['castingShort']
                    if u'director' in casting:
                        description += "Director : %s\n"%(casting['director'])
                    if u'actors' in casting:
                        description += "Actors : %s\n"%(casting['actors'])

                if u'synopsis' in entry:
                    description += "Synopsis : %s\n"%(re.sub("<[^>]+?>", 
                                                             "",
                                                             entry['synopsis']))
                poster = u""
                if 'poster' in entry:
                    value = entry["poster"]
                    if 'href' in value:
                        poster = value["href"]

                if poster == u"":
                    google = GoogleQuery()
                    poster = google.google_image(title)

                link = u''
                if 'link' in entry:
                    for elem in entry["link"]:
                        if 'rel' in elem:
                            if elem['rel'] == "aco:web":
                                link = elem['href']
                                break
                data.append(GoogleImdbResultCandidate(title,
                                                      link,
                                                      description,
                                                      poster,
                                                      year))
        return data
