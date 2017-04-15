Comparing TV Subreddit Communities
================

How diverse are people's TV taste? That is, do people tend to stick to watching shows belonging to one kind of genre, a few different genres, or many different genres?

To try to get at this question, I looked at reddit's various television communities (i.e., subreddits) and the commenting behavior of their members. If members were generally diverse in their TV taste, then we might find that they comment on shows across different genres. On the other hand, if their TV taste is a little bit narrower, they might tend to comment on shows that fall within the same genre.

I first needed to create a list of the different television subreddits. For this, I used the list compiled in the [r/television wiki](https://www.reddit.com/r/television/wiki/thelist). As you can see, the different shows have already been divided into four genres: Comedy, Animated, Drama, and Sci-Fi. While I don't think shows always fall into one category, I'll use r/television's categorization for now.

Next, I used python (see `Extracting_Television_Subreddits.py`) to interface with reddit's API to get the IDs of the different television subreddits. (I found using the ID codes rather than the subreddit name to be a more reliable identifier). I then created a table containing the different names of the subreddits, their ID code, and the genre that a subreddit belonged in (again, according to r/television). Using this table and some SQL code (see `Pulling_from_BigQuery.sql`), I queried the [dataset complied by /u/Stuck\_In\_the\_Matrix that's being hosted by /u/fhoffa on Google's BigQuery](https://www.reddit.com/r/bigquery/comments/3cej2b/17_billion_reddit_comments_loaded_on_bigquery/?st=j1dxknuq&sh=5a9cad8d). I pulled all the comments made between Jan 2015-Feb 2017 in those subreddits.

For information on how I further cleaned the data (and the logic behind the criteria I chose), please check out my `cleaning dataset` script. Essentially, I selected subreddits that had at least 5200 comments and selected authors/users that had commented on at least 2 subreddits and made at least 20 comments in a given subreddit.

We can first import the data file as well as load any needed libraries/packages.

``` r
library(dplyr)
library(magrittr)
library(reshape2)
library(entropy)
library(lsa)
library(ggplot2)

tv_subs<-read.table("tv_subreddit_comments(cleaned).txt", header=T, sep = "\t")
```

We can then group subreddits by genre and create composite comment scores, by genre, for each author/user.

``` r
tv_subs_sum<-tv_subs %>% group_by(author, Type) %>%
  summarise(Num_comments=sum(num_comments))

tvsubs_sum_w<-dcast(tv_subs_sum, author~Type, value.var="Num_comments", fill=0)
```

A quick preview of our new dataframe:

    ##                 author Animated Comedy Drama Sci-Fi
    ## 1 ______DEADPOOL______       38     51    21     49
    ## 2      ______LSD______        0     25    90      0
    ## 3    ___Redditsucks___       77      0     0     64
    ## 4              __bragg       92      0     0      0
    ## 5     __CaptainChaos__        0      0    63      0
    ## 6      __LordNibbler__       42      0   137      0

To get a sense of how diverse subreddit users are in terms of their TV taste, I'll be using a measure called "[entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory))." Entropy can be generally thought of as a measure of disorder or uncertainty; a score of 0 would indicate no uncertainty and for our context, no diversity.

Here, we'll use the `entropy` package to calculate the entropy for each author/user. I've also created a histogram plot that diagrams the frequency of individuals that fall into different entropy score bins.

``` r
tvsubs_entropy<-apply(tvsubs_sum_w[,-1], 1, entropy::entropy)
```

<img src="fComparing-TV-Subreddit-Communities_files/figure-markdown_github/histogram of entropy-1.png" style="display: block; margin: auto;" />

As one can see, while there is good number of people who show some diversity in their TV preference, there is also a substantial amount of people who only comment in only one genre (i.e., those who have an entropy score of 0). So let's focus our first follow-up analysis on these individuals.

Individuals who comment on only one genre
=========================================

First, we can ask, out of the four genres, do redditors prefer one particular genre?

``` r
entropy_zero_df<-tvsubs_sum_w[tvsubs_entropy==0,]

animated<-c()
comedy<-c()
drama<-c()
sci_fi<-c()

for (i in 1:length(entropy_zero_df$author)) {
  if (entropy_zero_df$Animated[i] > 0){
    animated<-c(animated, as.character(entropy_zero_df$author[i]))
  } else
    if (entropy_zero_df$Comedy[i] > 0) {
      comedy<-c(comedy, as.character(entropy_zero_df$author[i]))
    } else
      if (entropy_zero_df$Drama[i] > 0) {
        drama<-c(drama, as.character(entropy_zero_df$author[i]))
      } else sci_fi<-c(sci_fi, as.character(entropy_zero_df$author[i]))
}
```

    ## [1] "Number of individuals who comment only on animated shows: 2230"

    ## [1] "Number of individuals who comment only on comedies: 498"

    ## [1] "Number of individuals who comment only on dramas: 4420"

    ## [1] "Number of individuals who comment only on sci-fi shows: 989"

Dramas appear to be the most popular for this group, followed by animated shows, then sci-fi shows, with comedies involving the fewest "one-genrers."

The next question we can ask is whether people are also constrained within their genres. That is, do they tend to comment on a select few shows or do they comment on many different shows within the same genre. Again, we can calculate an individuals' entropy in the particular genre they only comment on.

``` r
Zero_ers<-list(Comedy=comedy, Drama=drama, Animated=animated, SciFi=sci_fi)
genre_id<-c()
entropy_sum<-c()

for (i in 1:length(Zero_ers)) {
    genre_df<-subset(tv_subs, author %in% unlist(Zero_ers[i]))
    genre_df_w<-dcast(genre_df, author~subreddit, value.var="num_comments", fill=0)
    genre_entropy<-apply(genre_df_w[-1], 1, entropy::entropy)
    genre_id<-c(genre_id, rep(names(Zero_ers[i]), length(genre_entropy)))
    entropy_sum<-c(entropy_sum, genre_entropy)
}

Zero_ers_sum_df<-data.frame(genre_id, entropy_sum)
```

Here is the histogram of entropy scores for each genre. Notice, here I'm plotting the *frequency* of individuals that fall within particular entropy bins.

<img src="Comparing-TV-Subreddit-Communities_files/figure-markdown_github/not normalized plot-1.png" style="display: block; margin: auto;" />

Here is another histogram of entropy scores for each genre. However, here, you'll notice that this plots the *proportion* of individuals that fall within the particular entropy bins. This is to account for the fact that the four genres differ in the number of individuals who are "one-genrers."

<img src="Comparing-TV-Subreddit-Communities_files/figure-markdown_github/nomralized plot-1.png" style="display: block; margin: auto;" />

Examining these histograms, it appears that while a large number of individuals are commenting on a couple shows of their preferred genre, there are nonetheless a substantial number of individuals who comment across multiple shows. So, like the overall pattern we found *across* genres, *within* a particular genre we see individuals who stick to a couple shows as well as a group of individuals showing more (although not overwhelming) diversity in their TV taste.

Given that there are individuals who do appear to stick to commenting on just a couple shows, a follow-up question would be to examine whether there are shows that users commonly enjoy together, such that commenting on one show would mean the user would also likely to comment on another. For example, one could imagine that there might be some overlap in those who comment on, say, the 30 Rock subreddit, and the Unbreakable Kimmy Schmidt subreddit (since they share same creators and the same sense of humor). To investigate this question, I performed a Latent Semantic Analysis on the individual shows that fall into each of the four genres. This analysis was inspired by the [FiveThirtyEight article that used this technique to gain insight to r/The\_Donald](https://fivethirtyeight.com/features/dissecting-trumps-most-rabid-online-following/). Essentially the analysis is used to quantify the amount of overlap in users/commenters across different subreddits.

I wrote a function that performs LSA on all the subreddits that belong to a particular genre. We just need to call the function for each of our genres.

``` r
subreddit_similarity<-function(genre) {

  genre_df<-subset(tv_subs, author %in% genre)
  genre_df_w<-dcast(genre_df, author~subreddit, value.var="num_comments", fill=0)

  #to calculate the tf-idf:
  subreddit_sums<-colSums(genre_df_w[,-1])
  tf_idf_pt1<-sweep(genre_df_w[,-1], 2, subreddit_sums, "/")
  tf_idf_pt2<-log((dim(genre_df_w)[2]-1)/rowSums(genre_df_w[,-1] !=0))
  tf_idf_full<-sweep(tf_idf_pt1, 1, tf_idf_pt2, "*")
  
  #to take cosine between the different subreddit pairs
  genre_sim<-round(cosine(as.matrix(tf_idf_full)), 3)
  
  #to return cosine values larger than absoluate value of 0.3. The cut-off here is somewhat arbitrary and you can choose to use a lower or higher cut-off
  top_genre_sim<-apply(genre_sim, 1, function(x) x[abs(x)>0.3 & abs(x)<1.0])
  return(top_genre_sim[lapply(top_genre_sim, length)>0])
  
}
```

We can first see what subreddits overlap in users/commenters for **animated** shows:

    ## [[1]]
    ## [1] "Animated shows:"
    ## 
    ## $americandad
    ## futurama 
    ##    0.359 
    ## 
    ## $futurama
    ## americandad 
    ##       0.359 
    ## 
    ## $gravityfalls
    ## stevenuniverse 
    ##          0.562 
    ## 
    ## $stevenuniverse
    ## gravityfalls 
    ##        0.562

Followed by **comedies**:

    ## [[1]]
    ## [1] "Comedy shows:"
    ## 
    ## $`30ROCK`
    ## KimmySchmidt 
    ##         0.53 
    ## 
    ## $bigbangtheory
    ## seinfeld 
    ##     0.76 
    ## 
    ## $brooklynninenine
    ## NewGirl 
    ##    0.32 
    ## 
    ## $DunderMifflin
    ## PandR 
    ## 0.328 
    ## 
    ## $KimmySchmidt
    ## 30ROCK 
    ##   0.53 
    ## 
    ## $LiveFromNewYork
    ##  Veep 
    ## 0.458 
    ## 
    ## $NewGirl
    ## brooklynninenine 
    ##             0.32 
    ## 
    ## $PandR
    ## DunderMifflin 
    ##         0.328 
    ## 
    ## $seinfeld
    ## bigbangtheory 
    ##          0.76 
    ## 
    ## $Veep
    ## LiveFromNewYork 
    ##           0.458

Then **dramas**:

    ## [[1]]
    ## [1] "Drama shows:"
    ## 
    ## $Daredevil
    ## JessicaJones 
    ##        0.451 
    ## 
    ## $FearTheWalkingDead
    ## thewalkingdead 
    ##          0.313 
    ## 
    ## $htgawm
    ## Scandal 
    ##   0.381 
    ## 
    ## $JessicaJones
    ## Daredevil 
    ##     0.451 
    ## 
    ## $orangeisthenewblack
    ## PeakyBlinders 
    ##         0.414 
    ## 
    ## $Outlander
    ## vikingstv 
    ##     0.477 
    ## 
    ## $PeakyBlinders
    ## orangeisthenewblack 
    ##               0.414 
    ## 
    ## $Scandal
    ## htgawm 
    ##  0.381 
    ## 
    ## $thewalkingdead
    ## FearTheWalkingDead 
    ##              0.313 
    ## 
    ## $vikingstv
    ## Outlander 
    ##     0.477

And finally, **sci-fi** shows:

    ## [[1]]
    ## [1] "Sci-fi shows:"
    ## 
    ## $FlashTV
    ## LegendsOfTomorrow 
    ##             0.407 
    ## 
    ## $LegendsOfTomorrow
    ## FlashTV 
    ##   0.407

Individuals who comment on more than one genre
==============================================

Lastly, we can re-focus our analysis on those individuals who commented on more than just one genre (i.e., those that had an entropy greater than 0). Here, I wanted to investigate to what extent preferences to different genres are correlated. That is, if an individual prefers to comment on animated shows, will they be more likely to comment on, say, comedy shows as well? For this, we'll just run a simple correlation on users'comment frequencies across the four genres.

``` r
entrop_nonzero_df<-tvsubs_sum_w[tvsubs_entropy >0, ]
print(cor(entrop_nonzero_df[,-1], method="spearman"))
```

    ##             Animated      Comedy      Drama     Sci-Fi
    ## Animated  1.00000000  0.05801708 -0.2325672 -0.3218939
    ## Comedy    0.05801708  1.00000000 -0.1742436 -0.3396559
    ## Drama    -0.23256724 -0.17424360  1.0000000  0.2352863
    ## Sci-Fi   -0.32189389 -0.33965588  0.2352863  1.0000000

From this, we see that when one comments on animated or comedy shows, they tend to be less likely to comment on dramas or sci-fi shows. Additionally, if one tends to comment on dramas, they are also more likely to comment on sci-fi shows (and vice versa).
