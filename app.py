"""

                                            Description of this project:

                    I want to create an web app built with Flask that'll check for the user's favorite
                    genre's and give them a list of animes to pick from.

                                            What will the Web App have?
                            
                                                1. An Anime Background

                                2. A form for the user to enter their favorite genres.

                    3. Once the user picked an anime from the generated list it will provide multiple links
                                                    to watch from 


                                4. A Nice Color Scheme of Purple and White

                            5. Display Synopes, Anime Cover and it's ranking
                     
                            
"""

from jikanpy import Jikan
from flask import Flask, render_template, request, url_for, redirect
import os



app = Flask(__name__,template_folder="templates")
app.static_folder = 'static'
app.jinja_options['extensions'].append('jinja2.ext.loopcontrols')

jikan = Jikan() # Create Jikan Object 

genres = {
"Action" : 1,
"Adventure":2,
"Cars":3 ,
"Comedy": 4,
"Dementia": 5,
"Demons" : 6,
"Drama": 8,
"Ecchi":9,
"Fantasy": 10,
"Game": 11,
"Harem": 35,
"Hentai" : 12,
"Historical":13,
"Horror": 14,
"Josei" : 43,
"Kids": 15,
"Magic": 16,
"Martial Arts": 17,
"Mecha": 18,
"Military": 38,
"Music":19,
"Mystery":7,
"Parody":20,
"Police":39,
"Psychological":40,
"Romance": 22,
"Samurai":21,
"School": 23,
"Sci-Fi":24,
"Seinen": 42,
"Shoujo":25,
"Shonen":27,
"Slice of Life": 36,
"Space": 29,
"Sports":30,
"Super Power":31,
"Supernatural":37,
"Thriller": 41,
"Vampire":32
}

referenceDict = {

}


@app.route('/')
def index():
    return render_template("index.html",genres=genres)

@app.route('/anime-list')
def displayAnime():
    # Retriving the information from the form with a GET REQUEST
    genre_one = request.args.get("first-select")
    genre_two = request.args.get("second-select")
    genre_three = request.args.get("third-select")

    # Multiple Words Cut Off
    if genre_one == 'Super':
        genre_one = 'Super Power'
    if genre_two == 'Super':
        genre_two = 'Super Power'
    if genre_three == 'Super':
        genre_three = 'Super Power'  

    if genre_one == 'Slice':
        genre_two = 'Slice of Life'
    if genre_two == 'Slice':
        genre_two = 'Slice of Life'
    if genre_three == 'Slice':
        genre_three = 'Slice of Life' 

    if genre_one == 'Martial':
        genre_one = 'Martial Arts'
    if genre_two == 'Martial':
        genre_two = 'Martial Arts' 
    if genre_three == 'Martial':
        genre_three = 'Martial Arts'

       

    # Declaring local and global variables
    global referenceDict
    getAnimes = []
    animeNames=[]
    animeImages = []
    storeOneTwo = []
    animeURLs = []
    rating = []
    synopsis = []
    results = 0
    animeInfo = {
        "anime":{

        },

        "urls":{

        }
        ,

        "images":{

        },
        "synopsis":{

        },

        "rating":{

        }
        
    }
 

    #  Want 5 pages of the genre to be searched
    firstPage = jikan.genre(type='anime', genre_id =genres[genre_one],page=1 )

    # Stores the first of the Anime information with the first genre
    for i in range(0,len(firstPage['anime'])):
        getAnimes.append(firstPage['anime'][i])  

    # Using try catches to avoid errors due to the different number of animes in a genre
    try:
        secondPage = jikan.genre(type='anime', genre_id =genres[genre_one],page=2 )
        for i in range(0,len(secondPage['anime'])):
            getAnimes.append(secondPage['anime'][i]) 
    except:
        pass
        
    try:
        thirdPage = jikan.genre(type='anime', genre_id =genres[genre_one],page=3 )
        for i in range(0,len(thirdPage['anime'])):
            getAnimes.append(thirdPage['anime'][i])  
    except:
        pass
    
    try:
        fourthPage = jikan.genre(type='anime', genre_id =genres[genre_one],page=4 )
        for i in range(0,len(fourthPage['anime'])):
            getAnimes.append(fourthPage['anime'][i])  
    except:
        pass
    
    try:
        fifthPage = jikan.genre(type='anime', genre_id =genres[genre_one],page=5 )
        for i in range(0,len(fifthPage['anime'])):
            getAnimes.append(fifthPage['anime'][i])  
    except:
        pass
 

    # Searching for the other 2 Genres to get the match
    for i in range(0,len(getAnimes)):
        for j in range(0, len(getAnimes[i]['genres'])):
            if getAnimes[i]['genres'][j]['name'] == genre_two or getAnimes[i]['genres'][j]['name'] == genre_three  :
                storeOneTwo.append(getAnimes[i])
                results+=1

    for i in range(0,len(storeOneTwo)):
            # Keeps everything the same size
            if len(storeOneTwo[i]['title']) > 25:
                temp = storeOneTwo[i]['title']
                shortenedName = temp[0:25]
                animeNames.append(shortenedName)
            else:
                animeNames.append(storeOneTwo[i]['title']) 
        
            animeURLs.append(storeOneTwo[i]['url']) # Stores the MyAnimeList URL
            rating.append(storeOneTwo[i]['score']) # Stores the rating from MyAnimeList
            animeImages.append(storeOneTwo[i]['image_url'])
            synopsis.append(storeOneTwo[i]['synopsis'])
                
    

    # Organizes into a dictionary of lists for other app.routes be able to use
    animeInfo['anime'] = animeNames
    animeInfo['urls'] = animeURLs
    animeInfo['images'] = animeImages
    animeInfo['synopsis'] = synopsis
    animeInfo['rating'] = rating
    referenceDict = animeInfo 
    # References the dictionary so other routes can use the data
    # Allows me to reference it because if I made the animeInfo global the information would stay with each request
    # The reference keeps the data new with each request because the animeInfo is a local dictionary  



    return render_template('animelist.html', animeNames=animeNames,animeImages=animeImages, results=results)


@app.route('/anime-details<id>')
def animeDetails(id):
    id = int(id)

    currentAnime = referenceDict['anime'][id] # Current Name of the Anime
    nineAnime = 'https://www12.9anime.to/search?keyword=' # link for searching on 9Anime
    planetAnime = 'https://www.anime-planet.com/anime/all?name=' # link for searching on 9Anime

    nineAnime = nineAnime + currentAnime.replace(' ','+') # replaces the whitespace with pluses and added it to the 9Anime link
    planetAnime = planetAnime + currentAnime.replace(' ', '%20') # replaces the whitespace with %20 and added it to the PlanetAnime link
    mal = referenceDict['urls'][id] # Current Link

    return render_template("animedetails.html",img=referenceDict['images'][id],name=referenceDict['anime'][id],synopsis=referenceDict['synopsis'][id],rating=referenceDict['rating'][id],mal=mal,nineAnime=nineAnime,planetAnime=planetAnime)
    


if __name__ == "__main__":
    app.run(debug = True)