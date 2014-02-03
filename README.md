suggest
=======

Suggest is a genre recommendation system based on how you listen to music during your daily activities.

Location and place data are gathered with every skip and play action to determine what you are doing. That information
is fed to the Suggest server which propogates the data to your unique user classification tree. Class data is then fed
into a recommender for most appropriate genre.

Data that is passed to server:
Location 1
Location 2 // determine speed
Percentage listened to of previous song
Current song playing

Data returned to android app:
Top 3 Genres //eventually song recommendation
