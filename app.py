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

from collections import OrderedDict
from jikanpy import Jikan
from flask import Flask, render_template, request, url_for, redirect


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
    # This is to ensure those words get properly placed in the API
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
    animeNames = []
    animeImages = []
    checkSecond = []
    animeURLs = []
    rating = []
    synopsis = []
    animes = OrderedDict()
    
    # I want to check as many pages as I can for the most results
    # Pages would never make it up to 50 so it will 100% throw an exception 
    # That means we collect all of the data from the API
    try:
        # Iterate through the pages of myanimelist genres
        pages = 1
        while pages<50:
            pageAnime = jikan.genre(type='anime', genre_id =genres[genre_one],page=pages)  
            # Stores all of the animes in a variable
            allAnimes  = pageAnime['anime'] 

            # Iterates through the list 
            # Stores relevant information into an ordered dictionary
            for i in allAnimes:
                # Creates a key
                animes[i['title']] = i
                # Stores all of the genres
                Allgenres = i['genres']

                # Creates another key with value as an ordered dict
                # Uses this to check if other genres are in this dictionary easily
                animes[i['title']]['genres'] = OrderedDict() 
                count = 0
                # Stores the genres in the dictionary
                for j in Allgenres:
                    animes[i['title']]['genres'][count] = j['name']
                    count+=1

            pages+=1 # new page
    except:
        pass

    # iterating through the keys to check if the other genres are in any animes
    for key in list(animes.keys()):
        checkGenres = animes[key]['genres']
  
        if genre_two not in checkGenres.values():
            animes.pop(key, None) # delete the key if it doesnt have those genres
        if genre_three not in checkGenres.values():
            animes.pop(key, None) 
     
    print(len(animes.keys()))
    # making the data more managable so it can be easily to implement with jinga notation
    animeNames = list(animes.keys())
    results = len(animeNames)
    for i in range(0,len(animeNames)):
        animeImages.append(animes[animeNames[i]]['image_url'])
        animeURLs.append(animes[animeNames[i]]['url'])
        rating.append(animes[animeNames[i]]['score'])
        synopsis.append(animes[animeNames[i]]['synopsis'])

        # Some names are very long so I want them to be shortened
        if len(animeNames[i]) > 25:
            temp = animeNames[i]
            shortenedName = temp[0:25]
            animeNames[i] = shortenedName

    

    # Organizes into a dictionary of lists for other app.routes be able to use
    referenceDict['anime'] = animeNames
    referenceDict['urls'] = animeURLs
    referenceDict['images'] = animeImages
    referenceDict['synopsis'] = synopsis
    referenceDict['rating'] = rating
 
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
    app.run()