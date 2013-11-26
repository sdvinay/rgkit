import argparse
import csv
import math

DEFAULT_ELO_SCORE = 1200

parser = argparse.ArgumentParser(description="Elo score calculator")

parser.add_argument("-i", "--input", help="Input file with scores in CSV", type=str)

#elo rank algorithm	 
def calculate_elo_rank(player_a_rank, player_b_rank, score, penalize_loser=True):
	if score[0] == score[1]:
		return (player_a_rank, player_b_rank)

	if score[0] > score[1]:
		winner_rank, loser_rank = player_a_rank, player_b_rank
	else:
		winner_rank, loser_rank = player_b_rank, player_a_rank

	rank_diff = winner_rank - loser_rank
	exp = (rank_diff * -1) / 400
	odds = 1 / (1 + math.pow(10, exp))
	if winner_rank < 2100:
		k = 32
	elif winner_rank >= 2100 and winner_rank < 2400:
		k = 24
	else:
		k = 16
	new_winner_rank = round(winner_rank + (k * (1 - odds)))
	if penalize_loser:
		new_rank_diff = new_winner_rank - winner_rank
		new_loser_rank = loser_rank - new_rank_diff
	else:
		new_loser_rank = loser_rank
	if new_loser_rank < 1:
		new_loser_rank = 1
	if score[0] > score[1]:
		return (new_winner_rank, new_loser_rank)
	else:
		return (new_loser_rank, new_winner_rank)

if __name__ == '__main__':
	args = parser.parse_args()
	botranks = {}
	with open(args.input, 'r') as scorefile:
		scorereader = csv.reader(scorefile)
		for row in scorereader:
			(bot1, bot2, score1, score2) = tuple(row)
			if bot1 not in botranks.keys(): botranks[bot1] = DEFAULT_ELO_SCORE
			if bot2 not in botranks.keys(): botranks[bot2] = DEFAULT_ELO_SCORE
			newranks =  calculate_elo_rank(botranks[bot1], botranks[bot2], (score1, score2))
			(botranks[bot1], botranks[bot2]) = newranks


	for bot in sorted(botranks, key=botranks.get, reverse=True):
		print botranks[bot], bot
