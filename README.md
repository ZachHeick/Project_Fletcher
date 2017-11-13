# Project Fletcher: Would Reddit Like My Comment?  
### Project 4 of Metis Data Science Bootcamp  

The fourth project at Metis focused on utilizing unsupervised and supervised learning techniques on datasets of our choice. One of my favorite social media platforms is Reddit, and for this project I was interested in looking at Reddit comments and their scores.  

### How Commenting Works on Reddit  

When users make comments on a submission, they are given an intial score of 1. From there, other users can either upvote (+1) or downvote (-1) the comment score. The intended use of this system was that users would upvote comments they found funny or was relevant and contributed well to discussion, while downvoting comments that were racist, sexist, or just not nice in general. Because Reddit sorts comment scores from greatest to least by default, the idea was that this upvote-downvote system would help hide nasty internet comments from discussion, and it does a pretty good job at this.  

### The Problem  

While the comment scoring system on Reddit is working as intended, users are also taking advantage of it as well. It is common across Reddit that if someone posts a genuine comment of an opinion that does not agree with the majority of Reddit users' opnions, that comment will be downvoted out of disagreement, eventually pushing the comment lower and lower down the submission page. The result is that many subreddits and submissions have become "echo chambers", where the same opinion or viewpoint is being iterated over and over again without any discussion from opposing sides.  

With this in mind, I wanted to see if I could predict how different subreddits view comments based on the context of the comment itself.  

---  

`Data_Files` contains pickle files used for collecting comments and modeling.  

`Project_Notebooks` contains two notebooks for this project:   

  1. `Get_Clean_Comments.ipynb`  
  2. `Project_Fletcher_Modeling.ipynb`  

`Scripts` contains a script for using the Reddit API to collect comments, pickle them, and store the comments in a MongoDB database hosted by AWS.  
  
`Web_App` contains the files for a simple flask application where users can select a subreddit and enter a comment and see how that subreddit would view the comment!   

![Flask App](https://github.com/ZachHeick/Project_Fletcher/blob/master/flask_app_screenshot.png)  
