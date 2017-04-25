README
================

Investigating diversity in TV taste using TV subreddits
=======================================================

This directory contains code for my investigations into how diverse people's TV tastes are, as reflected by the different subreddits they comment in. The main data was collected from [the reddit comments dataset compiled by /u/Stuck\_In\_the\_Matrix and hosted by /u/fhoffa on Google's BigQuery](https://www.reddit.com/r/bigquery/comments/3cej2b/17_billion_reddit_comments_loaded_on_bigquery/?st=j1dxknuq&sh=5a9cad8d). While most of the code involved was written in R, you'll notice that there is some Python and SQL code as well. In this directory you will find the following folders or files:

| Folder\_or\_File                                     | Description                                                                                                                                                                       |
|:-----------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Extracting Television Subreddits and Comments folder | Folder containing `Extracting_Television_Subreddits.py` and `Pulling_from_BigQuery.sql` scripts that detail how I obtained the dataset of comments across different TV subreddits |
| Cleaning\_dataset.md                                 | R Markdown file detailing how I cleaned the data after I collected it from BigQuery                                                                                               |
| Comparing-TV-Subreddit-Communities.md                | R Markdown file detailing the different analyses I performed to investigate the question regarding diversity in TV taste                                                          |
| Figures folder                                       | Contains the figures in `Comparing-TV-Subreddit-Communities.md`                                                                                                                   |


For a more detailed write up of the analyses, please visit: https://irischinresearch.wordpress.com/2017/04/16/how-diverse-are-peoples-tv-tastes/
