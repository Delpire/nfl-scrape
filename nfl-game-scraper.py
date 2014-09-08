#!/home/delpire/Downloads/dev/SCRAPY/bin/python

import scrapy

class Game(scrapy.Item):
  week_number = scrapy.Field()
  date = scrapy.Field()
  time = scrapy.Field()
  timezone = scrapy.Field()
  home_team = scrapy.Field()
  away_team = scrapy.Field()

class NFLSpider(scrapy.Spider):
  """Spider to pull all nfl games off www.nlf.com!"""
  name = 'nfl'
  start_urls = [ 'http://www.nfl.com/schedules']
  
  for i in range(1, 18):
    start_urls.append('http://www.nfl.com/schedules/2014/REG' + str(i))
  
  def parse(self, response):
    
    self.log('GETTING URL: %s' % response.url)
    
    schedule = response.css('.schedules-table')
    
    date = ''
    
    for item in schedule.css('li'):
      
      try:
      
        item_class = item.xpath('@class')[0].extract()
        
        if item_class == 'schedules-list-date':
          
          date = item.css('.' + item_class).css('span')[1].xpath('text()')[0].extract()
        
        else:
          
          game = Game()
          if 'REG' not in response.url:
            game['week_number'] = 1
          else:
            game['week_number'] = response.url.split("REG")[1]
          
          item_class = item_class.replace(' ', '.')
          center = item.css('.schedules-list-matchup').css('.list-matchup-row-center')
          game['time']=center.css('.list-matchup-row-time').css('.time').xpath('text()')[0].extract()
          game['date'] = date
          game['home_team'] = center.css('.list-matchup-row-anim').css('.list-matchup-row-team').css('.team-name.home').xpath('text()')[0].extract()
          game['away_team'] = center.css('.list-matchup-row-anim').css('.list-matchup-row-team').css('.team-name.away').xpath('text()')[0].extract()
          
          if "schedules-list-matchup.post" in item_class:
            game['timezone'] = 'N/A'
            
          else:
            game['time']+=center.css('.list-matchup-row-time').css('.suff').css('span')[1].xpath('text()')[0].extract()
            game['timezone']=center.css('.list-matchup-row-time').css('.suff').css('span')[2].xpath('text()')[0].extract()
          
          self.log('GETTING WEEK: %s' % (game['week_number']))
          self.log('GETTING DATE: %s' % (game['date']))
          self.log('GETTING TIME: %s' % (game['time']))
          self.log('GETTING TIMEZONE: %s' % (game['timezone']))
          self.log('GETTING HOME: %s' % (game['home_team']))
          self.log('GETTING AWAY: %s' % (game['away_team']))
          
          yield game
      except:
        self.log('ERROR')
    