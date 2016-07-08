import scrapy
import datetime
import facebook
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from MostPopularNews.items import MostpopularnewsItem
from bs4 import BeautifulSoup
import requests
import re

def nation_spider():
    #Get the Malawi nation page
    r = requests.get('http://www.mwnation.com')
    #Create Beatiful soup object
    soup = BeautifulSoup(r.content)
    #Get the element with title 'Most read today'
    most_read = soup.find(text=re.compile('Most Read Today'))
    most_read_tag = most_read.parent.parent.parent
    most_read_links = ''

    for link in most_read_tag.find_all('a', href=True):
        url = link.get('href')
        most_read_links += '\n' + url

    return most_read_links

def post_page(msg):
    graph = facebook.GraphAPI(
        'EAAM7NZAGek3MBAAAIBF1BfSx14TEINZAEGpIiZAGTPSDdry4IL9VeG9FwnciRa5zHSsWXY6S9JIggXP8SLtiRFhaWzNWuNA8ZCWUrtkuhhzkbipiwIiWI3AP7gZCMVo2USp9AA56riovCHZAY2Ak4HWNZAO4bpAhJMZD')
    graph.put_object('220018191725426', "feed", message=msg)

def post_facebook_wall(msg):
  # Fill in the values noted in previous steps here
  cfg = {
    "page_id"      : 220018191725426,  # Step 1
    "access_token" : 'EAAM7NZAGek3MBAAAIBF1BfSx14TEINZAEGpIiZAGTPSDdry4IL9VeG9FwnciRa5zHSsWXY6S9JIggXP8SLtiRFhaWzNWuNA8ZCWUrtkuhhzkbipiwIiWI3AP7gZCMVo2USp9AA56riovCHZAY2Ak4HWNZAO4bpAhJMZD'  # Step 3
    }

  api = get_api(cfg)
  status = api.put_wall_post(msg)

def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. You can skip
  # the following if you want to post as yourself.
  resp = graph.get_object('me/accounts')
  page_access_token = 'EAAM7NZAGek3MBAAAIBF1BfSx14TEINZAEGpIiZAGTPSDdry4IL9VeG9FwnciRa5zHSsWXY6S9JIggXP8SLtiRFhaWzNWuNA8ZCWUrtkuhhzkbipiwIiWI3AP7gZCMVo2USp9AA56riovCHZAY2Ak4HWNZAO4bpAhJMZD'
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

class NyasaSpider(BaseSpider):

    name = "nyasa"
    allowed_domains = ["nyasatimes.com"]
    start_urls = ["http://www.nyasatimes.com/"]

    def parse(self,response):
        # Lets put results in a string
        now = datetime.datetime.now()
        date = str(now.strftime("%A, %b %d, %Y"))
        bot_name = 'Brought to you by our newsbot @ \n https://www.facebook.com/funwithdata/?ref=aymt_homepage_panel'
        #Retrieve most commented articles
        comments = response.xpath('.//div[contains(@id,"comments")]')
        comments_today = comments.xpath('.//div[contains(@id,"sub11")]')
        most_commented_dy = comments_today.xpath('.//ul/li')[0]
        most_commented_dy_title = ' '.join(most_commented_dy.xpath('a/text()').extract())
        most_commented_dy_link = ' '.join(most_commented_dy.xpath('a/@href').extract())

        #Retrieve most popular
        popular = response.xpath('.//div[contains(@id,"popular")]')
        popular_today = popular.xpath('.//div[contains(@id,"sub21")]')
        most_popular_dy = popular_today.xpath('.//ul/li')[0]
        most_popular_dy_title = ' '.join(most_popular_dy.xpath('a/text()').extract())
        most_popular_dy_link = ' '.join(most_popular_dy.xpath('a/@href').extract())

        out_most_commented = 'Nyasatimes Most Commented Story Today-%s: %s \n %s \n %s'%(date, most_commented_dy_title,most_commented_dy_link,bot_name)
        out_most_popular = 'Nyasatimes Most Popular Story Today-%s: %s \n %s \n %s' % (date,most_popular_dy_title, most_popular_dy_link,bot_name)

        # print(out_most_commented)
        # print(out_most_popular)
        # #Finally we post to facebook
        post_facebook_wall(out_most_commented)
        post_facebook_wall(out_most_popular)
        #
        post_page(out_most_commented)
        post_page(out_most_popular)

        #post for the nation
        nation_links = nation_spider()
        #print (nation_links)

        #print ('The Nation News Paper Most Read Stories Today-%s: %s \n %s'%(date, nation_links, bot_name))
        post_facebook_wall('The Nation News Paper Most Read Stories Today-%s: %s \n %s'%(date, nation_links, bot_name))
        post_page('The Nation News Paper Most Read Stories Today-%s: %s \n'%(date, nation_links, bot_name))
