# Project Fletcher: Would Reddit Like My Comment?  
### Project 4 of Metis Data Science Bootcamp  

The fourth project at Metis focused on utilizing unsupervised and supervised learning techniques on datasets of our choice. One of my favorite social media platforms is Reddit, and for this project I was interested in looking at Reddit comments and their scores.  

### How Commenting Works on Reddit  

When a user makes a comment on a submission, they are given an intial score of 1. From there, other users can either upvote (+1) or downvote (-1) the comment score. The intention of this scoring system was that users would upvote comments they found funny or the comment was relevant and contributed well to discussion, while downvoting comments that were racist, sexist, or just not nice in general. Reddit sorts comment scores from greatest to least by default on all submissions, and the idea was that this upvote-downvote system would help hide nasty internet comments from discussion and promote positive comments. It does in fact do a really good job at this.  

### The Problem  

While the comment scoring system on Reddit is working as designed, users are also taking advantage of it as well. If someone posts a genuine comment giving an opinion that does not agree with the majority of Reddit users’ opinions, that comment will be downvoted out of disagreement, driving the comment score down and eventually pushing the comment out of default visability. This results in many subreddits and submissions becoming “echo chambers”; a place where the same opinion or viewpoint is being iterated over and over again without any discussion from opposing sides.  

With this in mind, I wanted to see if I could predict how different subreddits view comments based on the context of the comment itself.  

---  

`Data_Files` contains pickle files used for collecting comments and modeling.  

`Project_Notebooks` contains two notebooks for this project:   

  1. `Get_Clean_Comments.ipynb`  
  2. `Project_Fletcher_Modeling.ipynb`  

`Scripts` contains a script for using the Reddit API to collect comments, pickle them, and store the comments in a MongoDB database hosted by AWS.  
  
`Web_App` contains the files for a simple flask application where users can select a subreddit and enter a comment and see how that subreddit would view the comment!   

The blog post can be found [here](https://zachheick.github.io/2017/11/10/Would-Reddit-Like-My-Comment/).  

### Screenshot  

![Flask App](https://github.com/ZachHeick/Project_Fletcher/blob/master/flask_app_screenshot.png)  
