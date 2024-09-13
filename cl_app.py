# Music recommendation application
import csv

from utils import get_shape, get_minimum_and_maximum, read_from_file, get_top_artists



if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="Crisalov",
        description="Music recommendation application")

    parser.add_argument("-f", "--file", help="Path to the dataset file", required=True)
    parser.add_argument("-s", "--shape", action="store_true", help="Display the shape of the dataset")
    parser.add_argument("-ta", "--top-artists", type=int, default=5, help="Number of top artists to display (default: 5)")
    parser.add_argument("-m&m", "--min-max", type=int, help="Display the minimum and maximum values in a specific column")
    
    args = parser.parse_args(["-f", "./data/Spotify_Youtube.csv"])
    
    dataset_header, dataset = read_from_file()
    
 
    print(get_shape(dataset))
    print(get_minimum_and_maximum(dataset, 7))
    print(get_top_artists(dataset, 5))
    # print(~1)
    # print(~7)
    # print(1 if 2 > 3 else 1 if 5 < 2 else 4)
    # print([i if i % 2 == 0 else True for i in range(10)])
    
    
#! path to file ./data/Spotify_Youtube.csv