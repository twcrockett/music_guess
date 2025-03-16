import json
import os


def load_songs():
    """Load the existing songs from songs.json"""
    if os.path.exists('songs.json'):
        try:
            with open('songs.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: songs.json is not a valid JSON file.")
            return []
    else:
        print("Note: songs.json not found. A new file will be created.")
        return []


def save_songs(songs):
    """Save the songs list back to songs.json"""
    with open('songs.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, indent=2)
    print(f"Song collection saved. Total songs: {len(songs)}")


def add_song():
    """Add a new song to the collection"""
    print("\n=== Add New Song to Collection ===\n")

    # Get song details from user
    title = input("Enter song title: ").strip()
    artist = input("Enter artist name: ").strip()

    # Get and validate year
    while True:
        year_input = input("Enter release year: ").strip()
        try:
            year = int(year_input)
            if 1900 <= year <= 2025:  # Reasonable range check
                break
            else:
                print("Please enter a valid year between 1900 and 2025.")
        except ValueError:
            print("Please enter a valid year (numbers only).")

    # Skip confirmation and directly check for duplicates
    songs = load_songs()

    # Check for duplicates
    for song in songs:
        if song['title'] == title and song['artist'] == artist:
            print(f"Warning: This song appears to already exist in your collection.")
            confirm_anyway = input("Add it anyway? (y/n): ").lower()
            if confirm_anyway != 'y':
                return
            break

    # Add the new song
    new_song = {
        "title": title,
        "artist": artist,
        "year": year
    }

    songs.append(new_song)

    # Save the updated collection
    save_songs(songs)
    print(f"Successfully added '{title}' by {artist} to your collection.")


def main():
    while True:
        add_song()
        next_title = input("\nAdd another song? (y/n or enter next song title directly): ").strip()

        # If they entered 'n' or 'no', exit
        if next_title.lower() in ['n', 'no']:
            break

        # If they entered a title directly, use it to start the next song
        if next_title.lower() not in ['y', 'yes'] and next_title:
            # Load existing songs
            songs = load_songs()

            # Get the rest of the song details
            artist = input("Enter artist name: ").strip()

            # Get and validate year
            while True:
                year_input = input("Enter release year: ").strip()
                try:
                    year = int(year_input)
                    if 1900 <= year <= 2025:  # Reasonable range check
                        break
                    else:
                        print("Please enter a valid year between 1900 and 2025.")
                except ValueError:
                    print("Please enter a valid year (numbers only).")

            # Check for duplicates
            duplicate = False
            for song in songs:
                if song['title'] == next_title and song['artist'] == artist:
                    print(f"Warning: This song appears to already exist in your collection.")
                    confirm_anyway = input("Add it anyway? (y/n): ").lower()
                    if confirm_anyway != 'y':
                        duplicate = True
                    break

            if not duplicate:
                # Add the new song
                new_song = {
                    "title": next_title,
                    "artist": artist,
                    "year": year
                }

                songs.append(new_song)

                # Save the updated collection
                save_songs(songs)
                print(f"Successfully added '{next_title}' by {artist} to your collection.")
        # If they just entered 'y' or 'yes', the loop will continue to add_song()
        elif next_title.lower() not in ['y', 'yes']:
            # They entered something that's not 'y', 'n', or a title
            break

    print("Goodbye!")


if __name__ == "__main__":
    main()