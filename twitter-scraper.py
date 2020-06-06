# Importing necessary modules
import GetOldTweets3 as got
import pandas as pd
import sys
import argparse

# Part 0
# Processing arguments (type python twitter-scraper.py --help)
# ------------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--code", required=False, help="international country code")
ap.add_argument("-l", "--lang", required=False, help="international language code")
ap.add_argument("-f", "--file", required=False, help="file to save results to (format: filename.csv)")
ap.add_argument("-m", "--max", required=False, help="maximum number of tweets to scrape")
args = vars(ap.parse_args())

if args["code"]:
	code = args["code"]
else:
	code = "all"

if args["lang"]:
	lang = args["lang"]
else:
	lang = "ru"

if args["max"]:
	max = int(args["max"])
else:
	max = 0

file = args["file"]

# For testing purposes
#code = str(sys.argv[1])
#lang = str(sys.argv[2])

# Prepared country codes for the search query (more can be added in the future)
countries = {
	"kz": "казахстан",
	"uz": "узбекистан",
	"kg": "кыргызстан",
	"tj": "таджикистан",
	"tm": "туркменистан",
	"all": ""
}

# Selecting what country to use for the query in Part 1
country = countries[code]

# Part 1
# Getting tweets by keywords and date range
# Keywords are pre-coded for this particular study (this format was tested to get a maximum number of tweets)
# ------------------------------------------------------------------------------
tweetCriteria = got.manager.TweetCriteria()\
	.setQuerySearch(f"вирус китай {country} (коронавирус OR вирус OR китай OR {country}) lang:{lang}")\
	.setTopTweets(False)\
	.setEmoji("unicode")\
	.setSince("2020-01-01")\
	.setUntil("2020-06-10")\
	.setMaxTweets(max)

#.setNear("uzbekistan") - Twitter does not return any results if added

# Getting and storing data in "tweet" object
tweet = got.manager.TweetManager.getTweets(tweetCriteria)

# Part 2
# Organizing data in a CSV table
# ------------------------------------------------------------------------------
# Going through the object and constructing a table row by row
table_tweets = [[t.username,
	t.text,
	t.date,
	t.retweets,
	t.favorites,
	t.mentions,
	t.hashtags] for t in tweet]

# Storing the table in a Pandas data frame in order to export to file
tweet_df = pd.DataFrame(table_tweets, columns = ["User", "Tweet", "Date",
"Favorites", "Retweets", "Mentions", "Hashtags"])\
.sort_values("Date", ascending=False)

# Output the frame to CSV in current folder
if file:
	tweet_df.to_csv(f"{file}")
else:
	tweet_df.to_csv(f"tweets-{code}-{lang}.csv")

# HTML output (not needed, just a test)
#tweet_df.to_html("tweets.html")


