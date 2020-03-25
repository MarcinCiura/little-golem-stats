#!/usr/bin/python

import sys
import time
import urllib2
try:
  import BeautifulSoup
except ImportError:
  sys.exit(
      'See http://www.crummy.com/software/BeautifulSoup/#Download '
      'for instructions on installing Beautiful Soup 3.')

LITTLE_GOLEM = 'http://www.littlegolem.net/'


def PrintStats(gtid, plid):
  stats = {}
  response = urllib2.urlopen(
      LITTLE_GOLEM + 'jsp/info/player_game_list.jsp?gtid=%s&plid=%s' %
      (gtid, plid))
  soup = BeautifulSoup.BeautifulSoup(response.read())
  games = soup.findAll('table')[-1]
  rows = games.findAll('tr')
  for row in rows:
    cols = row.findAll('td')
    result = cols[-1].string
    if result is None:
      continue
    points = {'lost': 0, 'draw': 0.5, 'win': 1}[result]
    player = cols[1].string
    if player in stats:
      stats[player][0] += points
      stats[player][1] += 1
    else:
      stats[player] = [points, 1]
  tuples = stats.items()
  tuples.sort(key=lambda x: x[0].lower())
  tuples.sort(key=lambda x: x[1][1], reverse=True)
  print time.strftime('Results as of %Y-%m-%d')
  print '<table border="1" frame="box" rules="rows">'
  print '<tr><td><b>Opponent</b></td><td><b>Balance</b></td></tr>'
  for player, result in tuples:
    print '<tr><td>%s</td><td align="center">%s:%s</td></tr>' % (
        player.encode('utf-8'), result[0], result[1] - result[0])
  print '</table>'


def main():
  if len(sys.argv) < 3:
    sys.exit('Need two args: gtid player_id')
  gtid = sys.argv[1]
  plid = sys.argv[2]
  PrintStats(gtid, plid)


if __name__ == '__main__':
  main()
