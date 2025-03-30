import praw
import csv
import time

# Setting API credentials
CLIENT_ID = "MfMOMKSOoEtKaU8co4moqg"
CLIENT_SECRET = "KC3ZRdpFoMJLY3zxiq6phgY5mfEbRg"
USER_AGENT = "jamaica_tourism_scraper:v1.0 (by u/Firm-Message-2971)"
USERNAME = ""
PASSWORD = ""

# Praw library allows for connect to reddit API interaction
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
)

# Define the subreddit
subreddit_name = "JamaicaTourism"
subreddit = reddit.subreddit(subreddit_name)

# Write to a csv file to store the data
# with open("jamaica_tourism_data.csv", mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Title", "Comments"])  # Header row
#
#     # Fetch the top 50 posts from the subreddit
#     for post in subreddit.hot(limit=50):
#         post_comments = []
#
#         # Get top 10 comments
#         post.comments.replace_more(limit=0)  # Avoid "load more comments"
#         for comment in post.comments[:10]:  # Get top 5 comments
#             post_comments.append(comment.body)
#
#         # Write data to CSV
#         writer.writerow([post.title, " | ".join(post_comments)])

# Prepare CSV file
csv_filename = "jamaica_tourism_data.csv"
fieldnames = ["title", "selftext", "score", "num_comments", "url"]
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write CSV header

# Scraping variables
total_posts = 800  # number of posts I need
batch_size = 100  # Max limit per request (According to Reddit)
count = 0  # Track number of posts scraped
after = None  # Pagination marker

# Start scraping in batches of 100 since that is the limit.
while count < total_posts:
    print(f"Fetching posts {count} to {count + batch_size}...")
    retries = 3
    posts = []  # Initialize the posts list
    for _ in range(retries):
        try:
            # Fetch the posts
            posts = subreddit.top(limit=batch_size, time_filter="all") if after is None else subreddit.top(limit=batch_size,
                                                                                                           time_filter="all",
                                                                                        params={"after": after})
            break  # Exit the loop if successful
        except Exception as e:
            print(f"Error fetching posts: {e}. Retrying...")
            time.sleep(5)
    # Get the next batch of posts
    #posts = subreddit.new(limit=batch_size) if after is None else subreddit.new(limit=batch_size, params={"after": after})
    # if after is None, then we are on our first batch of posts, so we pass the batch size in the new method.
    # if after is not None, it means we are not on our first batch so I told rewrite to go for the next set of posts
    # this implements pagination and doesn't overwhelm the server. After helps me keep track of which post I'm at and getting more after it.
    if not posts:
        print("No new posts found or error fetching posts.")
        break  # Exit if no posts are returned
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        for post in posts:
            writer.writerow({
                "title": post.title,
                "selftext": post.selftext, # comments on a post
                "score": post.score, # upvotes - downvotes
                "num_comments": post.num_comments, # the number of comments under a post(shows popularity)
                "url": post.url
            })
            count += 1 #update count variable each time a post is scrapped.
            after = post.fullname   # Update pagination marker

    print(f"Scraped {count} posts so far...")
    print(f"Fetching next batch after {after}...")
    time.sleep(5)  # Sleep to avoid rate limits

print(f"Scraping complete! Saved {count} posts to {csv_filename}")