import requests
from bs4 import BeautifulSoup
import pprint
from operator import itemgetter

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.titleline > a')
subtext = soup.select('.subtext')

res_2 = requests.get('https://news.ycombinator.com/news?p=2')
soup_2 = BeautifulSoup(res_2.text, 'html.parser')
links_2 = soup_2.select('.titleline > a')
subtext_2 = soup_2.select('.subtext')

mega_links = links + links_2
mega_subtext = subtext + subtext_2

def sort_stories_by_votes(hnlist):
    new_list = sorted(hnlist, key=itemgetter('votes'), reverse=True)
    return new_list

def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))