#The following code was used to gather the different subreddits that were focused on particular TV shows.


#If you check out r/television's wiki page, there is a "Our Big List" page that lists out different television subreddits and the genres they belong in. While I don't necessarily think that television shows only belong to one category, for now, we'll use reddit's categorization.
#Note, given that r/television might be going through some changes, the look of the Big List page might be different. Shows might also be taken off or added as well. 


from bs4 import BeautifulSoup
import requests
import re
import praw
import pandas as pd



master_list_page = requests.get("https://www.reddit.com/r/television/wiki/thelist", headers={'User-agent': 'INSERT OWN USER AGENT HEADER'}) #note to include your own descriptive user agent header
print(master_list_page.status_code) #this is to make sure the request was successful

master_list_soup = BeautifulSoup(master_list_page.content, "html.parser")

subs_list=master_list_soup.blockquote



#Here, we want to go down the lists to extract the name of the different television subreddits as well as the genre they fall in. At the end of the for-loop, we'll have two lists -- one containing the subreddit names and one containing the genre information

show_list=[]
genre_list=[] 
tv_show_subs=[]
   
for element in subs_list.ul:
    if element.name== "li":
        for children in element:
            if children.name == "a":
                category=(children.text)
            if children.name == "ul":
                for link in children.find_all("a"):
                    show_list.append(link.get("href"))
        category2=[category]*len(show_list)
        genre_list.extend(category2)
        tv_show_subs.extend(show_list)
        show_list=[]



#You'll notice that the list also includes general TV subreddits (i.e., those that fall under the category of TV Reddit and Networks). Since we want subreddits that focus on a particular show, we'll exclude subreddits that belong in the "TV Reddit" and "Networks" categories. 

indexes=[i for i, sub in enumerate(genre_list) if sub not in ["TV Reddit", "Networks"]]

genre_list=genre_list[indexes[0]:indexes[-1]+1]
tv_show_subs=tv_show_subs[indexes[0]:indexes[-1]+1]



#Now to just clean some of the subreddit names so that we just get the title of the show and exclude the "/r/" portion.

subs_list_final=[]
    
for i, element in enumerate(tv_show_subs):
    tv_show_subs[i]=(re.sub(r'/r/', '', element))


#When I first started on this analysis, the r/television subreddit also had drop down menus for each of the genres (it no longer has that formatting). In those drop-down menus, I noticed there were additional shows that were not listed on the wiki page -- so I've added them here. 

genre_list.extend(["Comedy", "Comedy", "Comedy", "Comedy", "Animated", "Drama", "Drama", "Drama", "Drama", "Drama", "Sci-Fi", "Sci-Fi", "Sci-Fi", "Sci-Fi", "Sci-Fi", "Sci-Fi", "Sci-Fi", "Sci-Fi"])

tv_show_subs.extend(["crazyexgirlfriend", "FreshOfftheBoatTV", "JaneTheVirginCW", "Powerless", "YOI", "TwentyFour", "Brakebills", "Longmire", "TheNightOf", "UnRealTv", "BlackMirror", "legionfx", "RedDwarf", "StrangerThings", "TheOA", "Timeless", "Westworld", "ZNation"])



#From some preliminary work trying to query the large reddit comment database on BigQuery (thanks to /u/stuck_in_the_matrix and /u/fhoffa), I noticed that a subreddit's ID code was a more reliable identifier than the subreddit's name. To gather the ID codes quickly, I decided to interface with reddit's API.

reddit = praw.Reddit(client_id='YOUR CLIENT ID',
                     client_secret='YOUR CLIENT SECRET',
                     user_agent='YOUR USER AGENT HEADER') #note, you'll need to insert your own client_id and client_secret keys here.

sub_id=[]

for show in tv_show_subs:
    subreddit = reddit.subreddit(show)
    sub_id.append(subreddit.fullname)



#We can now combine the three different lists together to create a pandas dataframe and export it as a csv file. 

tv_sub_ids=[('ShowName', tv_show_subs),
            ('subreddit_id', sub_id),
            ('Type', genre_list)
            ]

tv_sub_df=pd.DataFrame.from_items(tv_sub_ids)
tv_sub_df.to_csv('television_subreddit_id.csv', index=False)