#!/usr/bin/env python2

import os
import ast
import argparse
import random
import math
import gc
###
import game
from settings import settings

parser = argparse.ArgumentParser(description="Robot game execution script.")
parser.add_argument("-m", "--map", help="User-specified map file.",
					default=os.path.join(os.path.dirname(__file__), 'maps/default.py'))
parser.add_argument("-c", "--count", type=int,
					default=1,
					help="Game count, default: 1")

parser.add_argument("-o", "--output", type=str, help="filename to write scores to")

def make_player(fname):
	with open(fname) as player_code:
		return game.Player(player_code.read())

def play(players):
	g = game.Game(*players, record_turns=True)
	for i in xrange(settings.max_turns):
		g.run_turn()

	return g.get_scores()

if __name__ == '__main__':

	args = parser.parse_args()

	map_name = os.path.join(args.map)
	map_data = ast.literal_eval(open(map_name).read())
	game.init_settings(map_data)

	botnames=[]
	bdir=os.listdir('../bots')
	for fn in bdir:
		botnames.append(fn)
	print botnames
	print '#of botnames',len(botnames)

	bots={}
	for bot in botnames:
		bots[bot] = make_player('../bots/'+bot)


	for i in xrange(args.count):
		if i % 100 == 0:
			gc.collect()
			
		random.shuffle(botnames)
		bot1 = botnames[0]
		bot2 = botnames[1]
		players = [bots[bot1], bots[bot2]]
		score = play(players)
		score_str = "{t1},{t2},{s1},{s2}".format(t1=bot1, t2=bot2, s1=score[0], s2=score[1])
		print "FINAL SCORE", score_str
		with open(args.output, 'a') as scorefile:
			scorefile.write(score_str + '\n')

