#!/usr/bin/env python

import webapp2
import urllib2
import codecs
import re
import sys
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
import lxml


class MainHandler(webapp2.RequestHandler):

	def get(self):

		podcast_rss = """<?xml version="1.0" encoding="utf-8" ?>
						<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
							<channel>
							<title>Nerdcore Podcast Scraper</title>
							<link></link>

							<itunes:author>Nerdy McNerdcore</itunes:author>
					        <itunes:owner>
					            <itunes:name>Nerdy McNerdcore</itunes:name>
					            <itunes:email>test@testmail.com</itunes:email>
							</itunes:owner>

					        <itunes:image href="http://www.nerdcore.de/wp-content/themes/NC12/images/moar.gif" />
					        <itunes:explicit></itunes:explicit>
					        <itunes:category text="">
					            <itunes:category text="" />
					        </itunes:category>

					        <itunes:summary>All the podcasts you'll find at Nerdcore.de</itunes:summary>

					        <category>Podcast</category>
					        <description>All the podcasts you'll find at Nerdcore.de</description>
					        
					        <language>en</language>
					        <copyright>Someone</copyright>
							<ttl></ttl>\n"""

		url = "http://www.nerdcore.de/tag/podcasts/feed/"
		urlfetch.set_default_fetch_deadline(600)

		response = urlfetch.fetch(url=url, follow_redirects=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'})
		content = response.content

		soup = BeautifulSoup(response.content, "xml")
		items = soup.find_all("encoded")
		for item in items:
			pubDate = item.parent.pubDate.text
			html = BeautifulSoup(item.string, "html.parser")
			anchors = html.find_all("a")
			for anchor in anchors:
				podcast_description = anchor.text
				podcast_url = anchor.attrs['href']

				if (podcast_description.find(".mp3") == -1 and podcast_url.find(".mp3") >= 0):
					item_string = "<item>\n"
					item_string += "\t<title>%s</title>\n" % podcast_description
					item_string += "\t<link>%s</link>\n" % podcast_url
					item_string += "\t<itunes:author>Nerdcore Podcast Link</itunes:author>\n"
					item_string += "\t<itunes:category text=\"Podcast\">\n"
					item_string += "\t\t<itunes:category text=\"Subcategory\" />\n"
					item_string += "\t</itunes:category>\n"
					item_string += "\t<category>Podcast</category>\n"
					item_string += "\t<duration>10</duration>\n"
					#item_string += "\t<description>%s</description>\n" % podcast_description
					item_string += "\t<pubDate>%s</pubDate>\n" % pubDate
					item_string += "\t<enclosure url=\"%s\" length=\"MB\" type=\"audio/mpeg\" />\n" % podcast_url
					item_string += "\t<guid>%s</guid>\n" % podcast_url
					item_string += "\t<author>Nerdy McNerdcore</author>\n"
					item_string += "</item>\n\n"
					podcast_rss += item_string

		podcast_rss += "</channel>\n"
		podcast_rss += "</rss>"

		self.response.write(podcast_rss)
		

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
