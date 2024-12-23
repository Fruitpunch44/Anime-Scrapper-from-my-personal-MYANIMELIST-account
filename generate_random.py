import random
import json
import os

# empty list to store shows
shows_to_watch = []


def generate(ani_list):
    num_shows = int(input("Enter the number of shows you want to check out: "))
    if not ani_list:
        print("No anime shows found.")
    else:
        # loop through the list with the provided range
        # append if not in shows to watch
        for _ in range(num_shows):
            show = random.choice(ani_list)
            if show not in shows_to_watch:
                shows_to_watch.append(show)
            else:
                print('show is already in watchlist')
    print("GENERATED SHOWS")


# save to JSON file
def save_list():
    output_file: str = input("enter file name: ")
    if not output_file.endswith('json'):
        print("you can only save in json format")
    else:
        with open(output_file, "w") as file:
            json.dump(shows_to_watch, file, indent=2)
        print(f'saved {output_file} to {os.getcwd()}')
