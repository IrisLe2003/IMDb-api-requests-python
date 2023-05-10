import requests

# Định nghĩa các thông tin đăng nhập liên quan đến RapidAPI
RAPIDAPI_KEY = "enter_your_key_here"
RAPIDAPI_HOST = "enter_your_host_here"

# Định nghĩa các thông tin header, bao gồm khóa đăng ký và máy chủ
headers = {
	"X-RapidAPI-Key": RAPIDAPI_KEY,
	"X-RapidAPI-Host": RAPIDAPI_HOST
}

search_string = ""
movie_id = ""
movie_title = ""
movie_year  = ""
top_cast_name = list()
top_crew_name = dict()
api_error = False

def search_movie(search_keyword):
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q": search_keyword}
    headers = {
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response

def search_cast(title_id):
    url = "https://imdb8.p.rapidapi.com/title/get-top-cast"
    querystring = {"tconst": title_id}
    headers = {
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response

def search_character(movie_id, name_id):
    url = "https://imdb8.p.rapidapi.com/title/get-charname-list"
    querystring = {
        "id": name_id, 
        "tconst": movie_id,
        "currentCountry":"US",
        "marketplace":"ATVPDKIKX0DER",
        "purchaseCountry":"US"}                   
    headers = {
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response

def search_crew(movie_id):
    url = "https://imdb8.p.rapidapi.com/title/get-top-crew"
    querystring = {"tconst":movie_id}
    headers = {
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response
    
def display_results():
    if not api_error:
        print("\nMovie Title:", movie_title)
        print("Release Year:", movie_year)
        print("\nCast:")
        for name in top_cast_name:
            print(name)
        print("\nCrew:")
        for role, names in top_crew_name.items():
            print(role.capitalize(), "-", ", ".join(names))
    else:
        print("API Error. Please try again later")


if __name__ == "__main__":
    try:
        while len(search_string) <= 2:
            search_string = input("\nEnter the movie name to search: ")
        print("Finding the best match for", search_string, "...")

        main_response = search_movie(search_string)
        if main_response.status_code == 200:
            response_data = main_response.json()
            if "results" in response_data:
                best_match = response_data["results"][0]
                movie_id = best_match["id"][7:-1]
                movie_title = best_match["title"]
                movie_year = str(best_match["year"])

                cast_response = search_cast(movie_id)
                if cast_response.status_code == 200:
                    top_cast_id = cast_response.json()[0:4]
                    for cast_id in top_cast_id:
                        char_response = search_character(movie_id, cast_id[6:-1])
                        if char_response.status_code == 200:
                            top_cast_name.append(char_response.json()[cast_id[6:-1]]["name"]["name"])
                        else:
                            print("Unable to fetch the character name for", movie_title)
                            
                else:
                    print("Unable to fetch the star cast for", movie_title)
                    api_error = True


                crew_response = search_crew(movie_id)
                if crew_response.status_code == 200:
                    response_data = crew_response.json()
                    for crew, details in response_data.items():
                        if len(details) > 0:
                            for data in details:
                                if crew not in top_crew_name:
                                    top_crew_name[crew] = []
                                top_crew_name[crew].append(data["name"])
                else:
                    print("Unable to fetch crew data for", movie_title)
                    api_error = True

                display_results()
        else:
            print("Invalid request or error in response")
            api_error = True
    except Exception as e:
        print("Error")
        print(e)

