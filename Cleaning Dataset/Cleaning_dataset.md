Cleaning the subreddit data
================

After we have extracted relevant comments from /u/Stuck\_In\_the\_Matrix's reddit dataset, we can import the file as well as load some packages needed for cleaning it.

``` r
library(dplyr)
library(magrittr)
library(reshape2)

tv_subs_users<-read.table("results_20170403.csv", sep=",", header=T)
dim(tv_subs_users)
```

    ## [1] 2020835       4

    ##            author     subreddit subreddit_id num_comments
    ## 1   sharkbaitzero       firefly     t5_2qs24            4
    ## 2    InvisibleEar      startrek     t5_2qixm          889
    ## 3       [deleted]   breakingbad     t5_2rlw4         9285
    ## 4          Jarrrp DunderMifflin     t5_2s9h3           77
    ## 5 StonedEaglesFan         arrow     t5_2u4js          174
    ## 6    Aquatic_Pyro  rickandmorty     t5_2u4lp            1

As you can see, there are four columns in the dataset: (1) the author/user that posted the comment, (2) the subreddit that the comment was made in, (3) the ID code of the subreddit, and (4) how many comments the author/user made in that particular subreddit.

The first thing we want to do is to get rid of users labelled as "\[deleted\]" and "AutoModerator." Those labelled as "\[deleted\]" are ones in which the original poster (or a moderator) decided to delete the comment -- hence, "\[deleted\]" contains a collection of users that had deleted their comment and thus is not a reliable metric for one individual poster's commenting activity. "AutoModerator" is not an actual user/poster but rather a bot that automatically makes a comment based on a subreddit's customization.

``` r
tv_subs_users<-subset(tv_subs_users, !author=="[deleted]" & !author=="AutoModerator")
```

We also want to remove any other types of bots. Bot usernames typically ends with the word "bot," so we'll use that as the criterion for exclusion. Note, this will inadvertently remove actual human users whose username end with the letters "bot," but from some of my preliminary analyses, I didn't find that too many of such occurrences. Additionally, given the large dataset that we have, I suspect this will have minimal impact on our analyses.

``` r
bot_list<-unique(grep("(?<!ro)bot$", tolower(tv_subs_users$author), perl=T, value=T))
tv_subs_users<-subset(tv_subs_users, !(author %in% bot_list))
```

For our later analyses, we will need to know which genre the different shows belong in so we should merge our current dataset with the table containing this information. (Note: to see how I generated this table, please refer to my `Extracting Television Subreddits` script.)

``` r
show_descrip<-read.table("television_subreddit_id.csv", sep=",", header=T)
tv_subs_users<-tv_subs_users %>%
  inner_join(show_descrip[,c("subreddit_id", "Type")], by="subreddit_id")
```

    ##            author     subreddit subreddit_id num_comments     Type
    ## 1   sharkbaitzero       firefly     t5_2qs24            4   Sci-Fi
    ## 2    InvisibleEar      startrek     t5_2qixm          889   Sci-Fi
    ## 3          Jarrrp DunderMifflin     t5_2s9h3           77   Comedy
    ## 4 StonedEaglesFan         arrow     t5_2u4js          174    Drama
    ## 5    Aquatic_Pyro  rickandmorty     t5_2u4lp            1 Animated
    ## 6      kiitsmotto     westworld     t5_2xhxq         1125   Sci-Fi

Okay, on to more cleaning!

Let's try to focus on reasonably sized subreddits, as a particularly small subreddit community might not be that informative. How does one decide what is considered "reasonably sized"? There are of course many different ways you can do this and you may disagree with the method and criteria that I have selected!

I first looked at the size of the subreddit based on the number of comments made in total. Television reddits often have discussion threads for each episode. This is not to say that users don't comment on other things regarding a TV show but my experience is that it is in these discussion threads that most of the commenting happens. A typical season in a television show can range somewhere from 13-20 episodes and given that we have about 2 years worth of comments, we might expect 26-40 episode discussion threads from a subreddit. We might then want to decide that at least 200 comments in a thread is considered a "good size" (again, this number is somewhat arbitrary). This would mean a reasonably sized/active subreddit should have a total of at least 200\*26 (i.e., 5200) comments. I therefore used this number as a cut-off mark.

``` r
comm_user_dist<-tv_subs_users %>%
  group_by(Type, subreddit) %>%
  summarise(Num_users=length(unique(author)),
            Total_comments=sum(num_comments)) %>%
  filter(Total_comments >=5200) %>%
  arrange(desc(Num_users))

tvsubs_top<-subset(tv_subs_users, subreddit %in% comm_user_dist$subreddit)
```

Next, we want to make sure we get users that are somewhat active. Again, we can use the approximate number of episode discussion threads (i.e., 26-40 across two years) as a metric. From this, we might want people who comment at least say maybe 20 comments per subreddit (assuming that one wouldn't always comment on every discussion thread).

``` r
tvsubs_top<-subset(tvsubs_top, num_comments >=20)
```

We also want users that have commented on more than one television subreddit so that we can compare the subreddits they choose to comment on (e.g., are they all part of the same genre or different genre).

``` r
author_preference<-tvsubs_top %>%
  group_by(author) %>%
  summarise(diff_subs=length(unique(subreddit))) %>%
  filter(diff_subs > 1) %>%
  arrange(diff_subs)

tvsubs_top<-subset(tvsubs_top, author %in% author_preference$author)
```

    ##                  author         subreddit subreddit_id num_comments   Type
    ## 3                Jarrrp     DunderMifflin     t5_2s9h3           77 Comedy
    ## 4       StonedEaglesFan             arrow     t5_2u4js          174  Drama
    ## 6            kiitsmotto         westworld     t5_2xhxq         1125 Sci-Fi
    ## 7             BearSpeak LegendsOfTomorrow     t5_37x73          298 Sci-Fi
    ## 9         beckoning_cat            Dexter     t5_2rahc           58  Drama
    ## 10 TotallyAwesomeDude12             arrow     t5_2u4js          184  Drama

Finally, we can output the cleaned dataframe into a tab-delimited text file for subsequent analyses.

``` r
write.table(tvsubs_top, file="tv_subreddit_comments(cleaned).txt", sep="\t", row.names=F, col.names = T)
```
