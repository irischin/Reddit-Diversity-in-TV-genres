{\rtf1\ansi\ansicpg1252\cocoartf1504\cocoasubrtf820
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww12200\viewh11360\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #Selects all comments made on relevant tv subreddits between Jan. 2015 to Feb. 2017 from the data extracted by /u/Stuck_In_the_Matrix and hosted by /u/fhoffa on BigQuery. \
#The relevant tv subreddits are listed in another BigQuery table that I created and uploaded. \
#See Extracting_Television_Subreddits.py for code on how I complied that table.\
\
SELECT author, subreddit, subreddit_id, COUNT(body) AS num_comments \
FROM (\
  SELECT * \
  FROM\
    [fh-bigquery:reddit_comments.2015_01],\
    [fh-bigquery:reddit_comments.2015_02],\
    [fh-bigquery:reddit_comments.2015_03],\
    [fh-bigquery:reddit_comments.2015_04],\
    [fh-bigquery:reddit_comments.2015_05], \
    [fh-bigquery:reddit_comments.2015_06], \
    [fh-bigquery:reddit_comments.2015_07], \
    [fh-bigquery:reddit_comments.2015_08], \
    [fh-bigquery:reddit_comments.2015_09], \
    [fh-bigquery:reddit_comments.2015_10], \
    [fh-bigquery:reddit_comments.2015_11], \
    [fh-bigquery:reddit_comments.2015_12], \
    [fh-bigquery:reddit_comments.2016_01],\
    [fh-bigquery:reddit_comments.2016_02],\
    [fh-bigquery:reddit_comments.2016_03],\
    [fh-bigquery:reddit_comments.2016_04],\
    [fh-bigquery:reddit_comments.2016_05], \
    [fh-bigquery:reddit_comments.2016_06], \
    [fh-bigquery:reddit_comments.2016_07], \
    [fh-bigquery:reddit_comments.2016_08], \
    [fh-bigquery:reddit_comments.2016_09], \
    [fh-bigquery:reddit_comments.2016_10], \
    [fh-bigquery:reddit_comments.2016_11], \
    [fh-bigquery:reddit_comments.2016_12],\
    [fh-bigquery:reddit_comments.2017_01], \
    [fh-bigquery:reddit_comments.2017_02]\
 )\
WHERE subreddit_id IN (\
  SELECT subreddit_id \
  FROM [subreddit-cluster-analysis:subreddit_tv_dist.television_subredit_ids]\
)\
GROUP BY author, subreddit, subreddit_id}