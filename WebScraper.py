from protego import Protego
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import requests
import re
import time
import json
import pronouncing
import nltk
import wordninja

__data = {}


def add_word(word):
    words = wordninja.split(word)
    for split_word in words:
        if __data.get(split_word) is not None:
            __data[split_word] += 1
        else:
            __data[split_word] = 1


def get_PoS(word):
    symbol = nltk.pos_tag([word])[0][1]
    if symbol in ['NN', 'NNS', 'NNP', 'NNPS']:
        return 'noun'
    elif symbol in ['CC']:
        return 'conjunction'
    elif symbol in ['FW']:
        return 'foreign word'
    elif symbol in ['JJ', 'JJR', 'JJS']:
        return 'adjective'
    elif symbol in ['PRP', 'PRP$']:
        return 'pronoun'
    elif symbol in ['RB', 'RBS', 'RBR']:
        return 'adverb'
    elif symbol in ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return 'verb'
    else:
        return 'other'


class RobotParser:
    def __init__(self, user_agent):
        self.user_agent = user_agent
        self.headers = {'user-agent': user_agent}
        print('RobotParser created with "' + user_agent + '"')
        self.created_RFPs = {}

    @staticmethod
    def __get_robot_url(url):
        split_url = urlsplit(url)
        robot_url = split_url.scheme + '://' + split_url.netloc + '/robots.txt'
        return robot_url

    @staticmethod
    def get_base_url(url):
        split_url = urlsplit(url)
        return split_url.scheme + '://' + split_url.netloc

    def __add_rfp(self, url, do_print=False):
        robot_url = self.__get_robot_url(url)
        if do_print:
            print('downloading from {0}...'.format(robot_url))
        r = requests.get(robot_url, headers=self.headers)
        if do_print:
            print('download completed [' + str(r.elapsed) + ']')
        rp = Protego.parse(r.text)
        self.created_RFPs[robot_url] = rp

    def can_fetch(self, url, do_print=False):
        robot_url = self.__get_robot_url(url)
        if self.created_RFPs.get(robot_url) is None:
            self.__add_rfp(url, do_print=do_print)
        if do_print:
            can_fetch = self.created_RFPs[robot_url].can_fetch(self.user_agent, robot_url)
            print('can_fetch: ' + str(can_fetch))
            return can_fetch
        else:
            return self.created_RFPs[robot_url].can_fetch(self.user_agent, robot_url)

    def read(self, url, do_print=False):
        robot_url = self.__get_robot_url(url)
        if self.created_RFPs.get(robot_url) is None:
            self.__add_rfp(url, do_print=do_print)
        return self.created_RFPs[robot_url].read(self.user_agent, robot_url)

    def crawl_delay(self, url, do_print=False):
        robot_url = self.__get_robot_url(url)
        if self.created_RFPs.get(robot_url) is None:
            self.__add_rfp(url, do_print=do_print)
        if do_print:
            crawl_delay = self.created_RFPs[robot_url].crawl_delay(self.user_agent)
            print('crawl_delay: ' + str(crawl_delay))
            return crawl_delay
        else:
            return self.created_RFPs[robot_url].crawl_delay(self.user_agent)

    def request_rate(self, url, do_print=False):
        robot_url = self.__get_robot_url(url)
        if self.created_RFPs.get(robot_url) is None:
            self.__add_rfp(url, do_print=do_print)
        if do_print:
            crawl_delay = self.created_RFPs[robot_url].request_rate(self.user_agent)
            print('request_rate: ' + str(crawl_delay))
            return crawl_delay
        else:
            return self.created_RFPs[robot_url].request_rate(self.user_agent)

    def site_maps(self, url, do_print=False):
        robot_url = self.__get_robot_url(url)
        if self.created_RFPs.get(robot_url) is None:
            self.__add_rfp(url, do_print=do_print)
        if do_print:
            site_maps = self.created_RFPs[robot_url].sitemaps
            print('site_maps: ')
            #            for entry in site_maps:
            #               print('> ' + entry)
            list(site_maps)
            return site_maps
        else:
            return self.created_RFPs[robot_url].request_rate(self.user_agent)

    def preferred_host(self, url, do_print=False):
        robot_url = self.__get_robot_url(url)
        if self.created_RFPs.get(robot_url) is None:
            self.__add_rfp(url, do_print=do_print)
        if do_print:
            pref_host = self.created_RFPs[robot_url].preferred_host
            print('preferred_host: ' + str(pref_host))
            return pref_host
        else:
            return self.created_RFPs[robot_url].preferred_host

    def print_all(self, url):
        self.can_fetch(url, do_print=True)
        self.crawl_delay(url, do_print=True)
        self.request_rate(url, do_print=True)
        self.site_maps(url, do_print=True)


class RobotFetcher:
    def __init__(self, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/97.0.4692.71 Safari/537.36'):
        self.userAgent = user_agent
        self.parser = RobotParser(user_agent=user_agent)

    def can_fetch(self, url):
        return self.parser.can_fetch(url)

    def fetch(self, url):
        if not self.parser.can_fetch(url):
            return None
        else:
            return requests.get(url, headers={'user-agent': self.userAgent})


def get_data():
    rf = RobotFetcher()
    index_pages = ['https://nytcrosswordanswers.org/nyt-crossword-puzzles/']
    for i in range(2, 101):
        index_pages.append(index_pages[0] + 'page/' + str(i) + '/')
    print(len(index_pages), 'pages queued.')
    for index_page in index_pages:
        print('Scraping: ', index_page, end=' ')
        pages = []
        soup = BeautifulSoup(rf.fetch(index_page).text,
                             'html.parser')
        paragraphs = soup.body.select('p.ast-the-content-more-link a')
        for entry in paragraphs:
            pages.append(entry['href'])
        for page in pages:
            soup = BeautifulSoup(rf.fetch(page).text, 'html.parser')
            answers = soup.body.select('div.nywrap ul span')
            for answer in answers:
                answer = str(answer)
                answer = re.sub('<span>', '', answer)
                answer = re.sub('</span>', '', answer)
                add_word(answer)
            time.sleep(1)
            print('.', end='')
        print(' Done')
        time.sleep(3)


def test():
    word1 = "hellothere"
    word2 = "generalKenobi"
    add_word(word1)
    add_word(word2)


def construct_dataset():
    temp = []
    for entry in __data.keys():
        phones = pronouncing.phones_for_word(entry)
        temp.append(
            {
                'word': entry,
                'count': __data[entry],
                'length': len(entry),
                'first-letter': entry[0],
                'last-letter': entry[len(entry) - 1],
                'phonemes': phones,
                'part-of-speech': get_PoS(entry),
            })
    return temp


if __name__ == "__main__":
    get_data()
    # print(__data)
    print(len(__data), 'unique words')
    __data = construct_dataset()
    with open('words.json', 'w') as fp:
        json.dump(__data, fp)
