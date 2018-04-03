I wanted to make a workout log, tracker, and accountability booster for the harvard women's ultimate frisbee club. But, it could be used by any frisbee team.
Over the break our team members are supposed to keep log their workout completion and make note of areas they feel they have improved in. It is mostly done on excel sheets.
I wanted to create a more unified, designed, intuitive, and informative platform. I think I have created a space which encourages partcipation and accountability, but also personal improvement.

I started work from the pset 7 distribution code. I wanted each team that used the site to have a login, but not individual user names because I wanted it to be a collective feeling entitity.
Teams share passwords and teams share their statistics. This makes letting teammates logs for eachother easier, but also makes for higher visiability and accountability. I considered each
user having theirown password so only they could see theirown stats, but then encouragement (and guilt) would be less. Moreover I want coaches to be able to see individual progress.

I choose to group tables in aggregate and not show each individually logged workout over time because I think it is more about the big picture and fast conveying of informaiton, though it is broken
between week data and all time data to give users a present idea and a sense of the magnitude of work that they and the team have put in. The home page is about the team and it's simplist goals, to have each of the
teammembers do every workout once a week and throw a frisbee every day.

The individual workout pages and logs are meant to be an informative space as well as a logging tool. They are a place where players can go to remind themselves of the sets. I did not originally start with the
individual workouts also logging the exercises that they contained, but I am glad that I added this feature because it allows the users to really see their progress over time.

the player page is meant to be informative and individually motivating. I did badges for a game like aspect, after you complete the goal, they appear as a physical (digital) manifestation of
the acheivement.

I tried to theme as much as possible with chart and workout page colors for intuitive recognition and style.

Figuring out how to pass php array information into charts and the correct sql selection took a significant amount of time. It is suprising how many things can go wrong in those, but once I figured them out,
each page design became easier.

I made sure to have a player entry page so that all of the other pages could simply have dropdown forms with names so that there wouldnt be duplicate logs because of misspelling.

Username: Quasar
pw: star

This username has good data, with diferent times, but not all of it was created after all the features were added to look at the site with, so there are some workouts without coordinated exercise logs.
I tried editing the date log in the data in another team page, but doing this changed information from int to floats

Youtube video: https://youtu.be/Fh8GkuRJsF8

Websites and distribuion code I looked at for help:
pset 7 distribution code
http://morrisjs.github.io/morris.js/ for morris charts
http://www.dofactory.com/  for sql syntax
http://www.color-hex.com/ for colors
https://www.w3schools.com/html/ for html form and paragraph syntax
