"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

"""
Right click on server
Open in Integrated terminal
type: python ser (tab)
enter

Right click on prove
Open in Integrate terminal
python .\\prove.py
enter
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0

class Request_Thread(threading.Thread):
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.response = {}
        self.status_code = {}

    def run(self):
        # global call_count
        # call_count += 1
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        self.status_code = response.status_code
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

def Get_One_Item(dict, index, url_so_far, threads, key):
    url = f'{url_so_far}{dict[f"{index}"]}'
    thread = Request_Thread(url)
    thread.start()
    threads[key].append(thread)

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    threads = {
       'chars':[],
       'planets':[],
       'starships':[],
       'vehicles':[],
       'species':[]
    }

    # TOP DATA
    top_data_thread = Request_Thread(TOP_API_URL)
    top_data_thread.start()
    top_data_thread.join()
    top_data = top_data_thread.response

    # REVENGE OF THE SITH DATA
    rots_url = f'{TOP_API_URL}{top_data["films"]}6'
    rots_data_thread = Request_Thread(rots_url)
    rots_data_thread.start()
    rots_data_thread.join()
    rots_data = rots_data_thread.response
    print('__________________________________________')
    log.write(rots_data)

    # CHARACTER THREADS
    char_data = rots_data["characters"]
    num_of_chars = len(char_data)
    for i in range(num_of_chars):
      Get_One_Item(char_data, i, rots_url, threads, 'chars')
        
    # PLANET THREADS
    planet_data = rots_data["planets"]
    num_of_planets = len(planet_data)
    for i in range(num_of_planets):
      Get_One_Item(planet_data, i, rots_url, threads, 'planets')

    # STARSHIP THREADS
    starship_data = rots_data["starships"]
    num_of_starships = len(starship_data)
    for i in range(num_of_starships):
      Get_One_Item(starship_data, i, rots_url, threads, 'starships')

    # VEHICLE THREADS
    vehicle_data = rots_data["vehicles"]
    num_of_vehicles = len(vehicle_data)
    for i in range(num_of_vehicles):
      Get_One_Item(vehicle_data, i, rots_url, threads, 'vehicles')

    # SPECIES THREADS
    species_data = rots_data["species"]
    num_of_species = len(species_data)
    for i in range(num_of_species):
      Get_One_Item(species_data, i, rots_url, threads, 'species')

    # JOIN THREADS AND SORT LISTS
    chars = []
    for thread in threads['chars']:
       thread.join()
       chars.append(thread.response['name'])
    chars.sort()

    planets = []
    for thread in threads['planets']:
       thread.join()
       planets.append(thread.response['name'])
    planets.sort()

    starships = []
    for thread in threads['starships']:
       thread.join()
       starships.append(thread.response['name'])
    starships.sort()

    vehicles = []
    for thread in threads['vehicles']:
       thread.join()
       vehicles.append(thread.response['name'])
    vehicles.sort()

    species = []
    for thread in threads['species']:
       thread.join()
       species.append(thread.response['name'])
    species.sort()

    # LOG EVERYTHING
    log.write(f'Characters: {num_of_chars}')
    log.write(chars)

    log.write(f'Planets: {num_of_planets}')
    log.write(planets)

    log.write(f'Starships: {num_of_starships}')
    log.write(starships)

    log.write(f'Vehicles: {num_of_vehicles}')
    log.write(vehicles)

    log.write(f'Species: {num_of_species}')
    log.write(species)

    # END LOG
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()