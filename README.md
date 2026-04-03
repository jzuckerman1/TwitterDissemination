# TwitterDissemination

CS395 Project. This project constructed by James Zuckerman. We investigate how president's and figures of power's tweets affect market movement and uncertainty. We consider how the title of Presidency shapes ripples across the market. 

## How to run

Code is currently concentrated in `prelim_analysis.ipynb`. This file can be run as a jupyter notebook with some baseline visuals indicating how the presidency changes tweets. it examines Obama and Trump and how the market impact of their tweets differs.

## File Structure

```
./TwitterDissemination
|-- /data
|   |--obama.csv                        # Obama tweets [1]
|   |--rollcall_social_posts.csv        # Trump tweets and Truth.com from [2] 
|   |--trump_tweets.csv                 # Trump tweets from [3]
|   |--VIX_DAILY.csv                    # Daily values in the VIX
|-- /scripts
|   |--rollcall_scraper.py              # Scraper for rollcall website
|   |--yahoo_finance_data_grabber.py    # Scraper for yahoo finance data 
|--.gitignore
|--prelim_analysis.ipynb                # Preliminary analysis of data
|--README.md                            # This markdown document
```

## Links for data

The following links may be used to find the data we used for our project:

1. [Obama Tweets from Kaggle](https://www.kaggle.com/datasets/neelgajare/all-12000-president-obama-tweets)
2. [RollCall Media Posts](https://rollcall.com/factbase/trump/topic/social/?platform=all&sort=date&sort_order=desc&page=1)
2. [Trump Tweets from Kaggle](https://www.kaggle.com/datasets/codebreaker619/donald-trump-tweets-dataset)
