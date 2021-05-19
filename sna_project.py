import praw
import matplotlib.pyplot as plt
import networkx as nx
import pickle
from prawcore.exceptions import Forbidden
from datetime import datetime
import time

NUM_OF_SUBREDDITS = 1000
NUM_OF_USERS_PER_SUBREDDIT = 100
NUM_OF_POSTS_PER_USER = 50
ERRORCOUNT_1 = 0
ERRORCOUNT_2 = 0
MAX_LOOP = 0

#secret = l2lkbw5xrjyHqUhHH3-U8JbxFDlwuA
#client_id = N0yT2MUgrlY2bg
def run():
	global MAX_LOOP
	global ERRORCOUNT_1, ERRORCOUNT_2
	now = datetime.now()
	print("running")
	r = praw.Reddit(user_agent='sna_project_acc',
					client_id='N0yT2MUgrlY2bg', 
					client_secret='l2lkbw5xrjyHqUhHH3-U8JbxFDlwuA',
					)
	#r.login('mikarvon18', 'hessuhopo')
	r.read_only = True

	top_subreddits = []

	submissions = r.subreddit('all').hot(limit=None)
	for submission in submissions:
		subreddit = submission.subreddit
		print(subreddit)
		if len(top_subreddits) >= NUM_OF_SUBREDDITS:
			break
		if subreddit not in top_subreddits:
			top_subreddits.append(subreddit)
	print()
	for i in top_subreddits:
		print(i)

	subreddit_users = [[]]
	i = 0
	loop = 0
	for num, subreddit in enumerate(top_subreddits):
		print(f"Loop: {loop}")
		loop+=1
		c = 0
		#print(subreddit)
		submissions = r.subreddit(str(subreddit)).hot(limit=NUM_OF_USERS_PER_SUBREDDIT*1.15)
		#print(subreddit, num)
		#print(i)
		#i+=1
		subreddit_users[num].append(subreddit)
		for submission in submissions:
			try:
				#print(submission.url)
				if hasattr((submission.author), 'is_suspended'):
					continue
			except:
				ERRORCOUNT_1 += 1
				print("Exception.....")
				continue
			#print(f"c: {c}")
			if c >= NUM_OF_USERS_PER_SUBREDDIT:
				break

			if submission.stickied:
				#print("STICKIED!!!!")
				continue
			else:
				subreddit_users[num].append(submission.author)
				c+=1
			
			#print(submission.title)
		
		subreddit_users.append([])
	subreddit_users.pop()
	linked_subreddits = [[]]
	try:
		for num, user_list in enumerate(subreddit_users):
			print(f"loop: {num}-{len(subreddit_users)}")
			MAX_LOOP += 1

			#print(user_list)
			#temp_subreddit = user_list.pop()
			#print(f"Subreddit: {temp_subreddit}")
			#print()
			for i, user in enumerate(user_list):
				

				if i == 0:
					#print(f"Subreddit: r/{user}")
					linked_subreddits[num].append(str(user))
					orig_subreddit = user
				else:
					#user_list[i].append([])
					#print(f"{i}. u/{user}")
					try:
						redditors_submissions = r.redditor(str(user)).submissions.new(limit=NUM_OF_POSTS_PER_USER)
					except:
						print(f"***ERROR***")
						ERRORCOUNT_2 += 1
					for submission in redditors_submissions:
						try:
							subred_str = str(submission.subreddit)
						except:
							print(f"***ERROR***")
							ERRORCOUNT_2 += 1
							continue
						#print(f"r/{submission.subreddit}")
						#print(f"Title: {submission.title}, upvote ratio: {submission.upvote_ratio}, url: {submission.url}")
						if (subred_str[0] == 'u') and (subred_str[1] == '_'):
							#print(f"LÖYTY U!!!, {submission.subreddit}")
							continue
						elif subred_str == orig_subreddit:
							#print(f"SAMA SUBREDDIT!!!")
							continue
						elif subred_str in linked_subreddits[num]:
							continue
						else:
							linked_subreddits[num].append(subred_str)
							#pass
							

				#pass
			linked_subreddits.append([])
	except:
		print("******ERROR*********")
		ERRORCOUNT_2 += 1
	linked_subreddits.pop()
	for i in linked_subreddits:
		print(i)

	with open(f'data-{now.strftime("%b-%d-%Y--%H-%M")}__{str(NUM_OF_SUBREDDITS)}-{str(NUM_OF_USERS_PER_SUBREDDIT)}-{str(NUM_OF_POSTS_PER_USER)}.txt', 'wb') as fp:
	    pickle.dump(linked_subreddits, fp)
	"""

	submissions = r.subreddit('python').top(limit=1)
    l = 0
	for submission in submissions:
        print(f"loop: {l}")
        l+=1
		#print(submission.title)
		top_comments = list(submission.comments)
		
		for comment in top_comments:
			post_user = comment.author
			#print(f"User: {post_user} Comment:{comment.body}")
			#print()
			#print(f"All posts of User: {post_user}:")
			redditor_posts = r.redditor(str(post_user)).submissions.hot(limit=1)
			for post in redditor_posts:
				if post.subreddit == ('Python'):

					print(f"********** User has post in r/python: {post.title}")

			#print(redditor_posts[1])
		#submission = next(submissions)

	"""
def main():
	global ERRORCOUNT
	start = time.time()
	run()
	print(f"Total run time: {(time.time() - start):2f}")
	print(f"Total num of errors in first part: {ERRORCOUNT_1}, In second: {ERRORCOUNT_2}, Finished in loop: {MAX_LOOP}/{NUM_OF_POSTS_PER_USER}")

if __name__ == '__main__':
	main()