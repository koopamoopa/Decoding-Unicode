import requests 
import re
from typing import List, Tuple

# Handles the fetching of data from the google doc, then handles the responses 
# to getting and handling the column data and displaying the characters
def display_grid_from_url(url: str) -> None:
    # fetch the document content
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
    except requests.RequestException as e:
        print(f"Error fetching document: {e}")
        return
    
    # parse the character data from the document into a list that contains each character's position
    characters = parse_sequential_format(content)
    
    if not characters: # no characters found
        print("No character data found in the document")
        return
    
    # create and print the grid
    grid = create_grid(characters)
    print_grid(grid)

# find the table in the google doc, and put them into a list of each row
def parse_sequential_format(content: str) -> List[Tuple[int, str, int]]:
    characters = [] # return list
    
    # remove HTML tags and get plain text
    text = re.sub(r'<[^>]+>', '\n', content)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # find where the data starts (after headers aka after x-coordinate)
    firstDataIndex = 0
    for i in range(len(lines) - 2):
        # Check if three consecutive lines match the expected headers
        if (lines[i].strip().lower() == 'x-coordinate' and
            lines[i+1].strip().lower() == 'character' and
            lines[i+2].strip().lower() == 'y-coordinate'):
            firstDataIndex = i + 3  # Skip the three header lines
            break
    
    # parse data in groups of three: x, char, y and store into return list
    i = firstDataIndex
    while i + 2 < len(lines):
        try:
            x = int(lines[i])
            char = lines[i + 1]  if lines[i + 1] else ' ' # make blank if character has nothing
            y = int(lines[i + 2])
            characters.append((x, char, y))
            i += 3
        except (ValueError, IndexError): # continue on error
            i += 1
    
    return characters

# creates the grid based on the character location list
def create_grid(characters: List[Tuple[int, str, int]]) -> List[List[str]]:
    if not characters:
        return []
    
    # find and set the size of the grid
    max_x = max(x for x, _, _ in characters)
    max_y = max(y for _, _, y in characters)
    
    # initialise an empty grid
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # place each specified character in their x and y position in the grid
    for x, char, y in characters:
        if 0 <= x <= max_x and 0 <= y <= max_y:
            grid[max_y - y][x] = char # invert 
    
    return grid

# print the created grid
def print_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print(''.join(row).rstrip())



if __name__ == "__main__":
    # https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub
    # https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub

    url = input("Enter the URL of the Google Doc to display the grid: ")
    print("-" * 30)
    display_grid_from_url(url)