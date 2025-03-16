import json
import random
from datetime import datetime, timedelta
import os


class SongCurator:
    def __init__(self, songs_file="songs.json", curated_file="curated_songs.json"):
        self.songs_file = songs_file
        self.curated_file = curated_file
        self.all_songs = []
        self.curated_songs = {}
        self.load_files()

    def load_files(self):
        """Load the songs and curated_songs JSON files"""
        try:
            with open(self.songs_file, 'r', encoding='utf-8') as f:
                self.all_songs = json.load(f)
            print(f"Loaded {len(self.all_songs)} songs from {self.songs_file}")

            try:
                with open(self.curated_file, 'r', encoding='utf-8') as f:
                    self.curated_songs = json.load(f)
                print(f"Loaded curated songs for {len(self.curated_songs)} dates")
            except FileNotFoundError:
                print(f"No existing {self.curated_file} found. Will create a new one.")
                self.curated_songs = {}
        except Exception as e:
            print(f"Error loading files: {e}")
            exit(1)

    def save_curated_songs(self):
        """Save the curated songs back to the JSON file"""
        with open(self.curated_file, 'w', encoding='utf-8') as f:
            json.dump(self.curated_songs, f, indent=2)
        print(f"Saved curated songs to {self.curated_file}")

    def get_used_song_ids(self):
        """Get a set of all song IDs that have already been used in curated_songs"""
        used_songs = set()
        for date, songs in self.curated_songs.items():
            for song in songs:
                # Create a unique identifier for each song
                song_id = f"{song['title']}|{song['artist']}"
                used_songs.add(song_id)
        return used_songs

    def search_songs(self, query):
        """Search for songs by title or artist"""
        query = query.lower()
        results = []

        for i, song in enumerate(self.all_songs):
            if query in song['title'].lower() or query in song['artist'].lower():
                results.append((i, song))

        return results

    def display_search_results(self, results):
        """Display search results with numbers for selection"""
        if not results:
            print("No songs found matching your search.")
            return

        print(f"\nFound {len(results)} matching songs:")
        for i, (idx, song) in enumerate(results):
            print(f"{i + 1}. {song['title']} by {song['artist']} ({song['year']})")

    def add_songs_for_date(self, date_str=None):
        """Add 5 songs for a specific date"""
        if date_str is None:
            # Use today's date if none provided
            date_str = datetime.now().strftime("%Y-%m-%d")

        # Check if date already exists
        if date_str in self.curated_songs:
            print(f"Warning: {date_str} already has {len(self.curated_songs[date_str])} songs curated.")
            action = input("Do you want to (r)eplace, (a)dd more, or (c)ancel? ").lower()
            if action == 'c':
                return
            elif action == 'r':
                self.curated_songs[date_str] = []
            # For 'a', we'll just continue and add more
        else:
            self.curated_songs[date_str] = []

        # Get songs that have already been used
        used_songs = self.get_used_song_ids()

        # How many more songs we need to add
        needed = 5 - len(self.curated_songs[date_str])

        selections = []
        while len(selections) < needed:
            # Allow user to search or get random suggestions
            print(f"\n{len(selections)}/{needed} songs selected for {date_str}")
            choice = input("Enter search term, 'r' for random suggestions, or 'done' to finish: ")

            if choice.lower() == 'done':
                break
            elif choice.lower() == 'r':
                # Show random suggestions, avoiding already used songs
                unused_songs = [(i, song) for i, song in enumerate(self.all_songs)
                                if f"{song['title']}|{song['artist']}" not in used_songs]

                if not unused_songs:
                    print("No unused songs left!")
                    continue

                sample_size = min(10, len(unused_songs))
                suggestions = random.sample(unused_songs, sample_size)
                self.display_search_results(suggestions)

                selection = input("Enter the number to select, 'n' for new suggestions, or press Enter to skip: ")
                if selection.lower() == 'n':
                    continue
                elif selection.isdigit() and 1 <= int(selection) <= len(suggestions):
                    song_idx = int(selection) - 1
                    selected_song = suggestions[song_idx][1]
                    self.curated_songs[date_str].append(selected_song)
                    used_songs.add(f"{selected_song['title']}|{selected_song['artist']}")
                    selections.append(selected_song)
                    print(f"Added: {selected_song['title']} by {selected_song['artist']}")
            else:
                # Search for songs with the given term
                results = self.search_songs(choice)
                self.display_search_results(results)

                if not results:
                    continue

                selection = input("Enter the number to select or press Enter to skip: ")
                if selection.isdigit() and 1 <= int(selection) <= len(results):
                    song_idx = int(selection) - 1
                    selected_song = results[song_idx][1]
                    song_id = f"{selected_song['title']}|{selected_song['artist']}"

                    if song_id in used_songs:
                        print("This song has already been used in your curated list.")
                        use_anyway = input("Use it anyway? (y/n): ").lower() == 'y'
                        if not use_anyway:
                            continue

                    self.curated_songs[date_str].append(selected_song)
                    used_songs.add(song_id)
                    selections.append(selected_song)
                    print(f"Added: {selected_song['title']} by {selected_song['artist']}")

        # Save after adding songs for this date
        if selections:
            self.save_curated_songs()
            print(f"Added {len(selections)} songs for {date_str}")

    def find_next_unaccounted_date(self):
        """Find the next unaccounted for date based on existing curated dates"""
        # Get all existing dates
        existing_dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in self.curated_songs.keys()]

        if not existing_dates:
            # If no dates exist yet, start with today
            return datetime.now().strftime("%Y-%m-%d")

        # Sort dates to find the latest one
        existing_dates.sort()
        latest_date = existing_dates[-1]

        # Start checking from the day after the latest date
        next_date = latest_date + timedelta(days=1)

        # Return the next date, including future dates
        return next_date.strftime("%Y-%m-%d")

    def show_curated_songs(self):
        """Display all curated songs by date"""
        if not self.curated_songs:
            print("No curated songs yet.")
            return

        for date in sorted(self.curated_songs.keys()):
            songs = self.curated_songs[date]
            print(f"\n{date} ({len(songs)} songs):")
            for i, song in enumerate(songs):
                print(f"  {i + 1}. {song['title']} by {song['artist']} ({song['year']})")

    def suggest_theme(self, date_str=None):
        """Suggest a theme based on songs for a date"""
        if date_str is None:
            # Find the most recent date
            dates = sorted(self.curated_songs.keys())
            if not dates:
                print("No curated songs to analyze.")
                return
            date_str = dates[-1]

        if date_str not in self.curated_songs:
            print(f"No songs found for {date_str}")
            return

        songs = self.curated_songs[date_str]
        if len(songs) < 3:
            print(f"Not enough songs for {date_str} to suggest a theme.")
            return

        # Look for themes:
        # 1. Same decade
        decades = {}
        for song in songs:
            decade = (song['year'] // 10) * 10
            decades[decade] = decades.get(decade, 0) + 1

        main_decade = max(decades.items(), key=lambda x: x[1])
        if main_decade[1] >= 3:
            print(f"Suggested theme: Music from the {main_decade[0]}s")
            return

        # 2. Look for common words in titles
        words = {}
        for song in songs:
            for word in song['title'].lower().split():
                if len(word) > 3:  # Skip short words
                    words[word] = words.get(word, 0) + 1

        common_words = [word for word, count in words.items() if count > 1]
        if common_words:
            print(f"Common words in titles: {', '.join(common_words)}")

        # Default message
        print("These songs are quite diverse! No clear theme detected.")


def main():
    curator = SongCurator()

    while True:
        print("\n--- Song Curator Menu ---")
        print("1. Add songs for a specific date")
        print("2. Add songs for today")
        print("3. Add songs for next unaccounted date")
        print("4. Show all curated songs")
        print("5. Suggest theme for a date")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            date_str = input("Enter date (YYYY-MM-DD): ")
            curator.add_songs_for_date(date_str)
        elif choice == '2':
            today = datetime.now().strftime("%Y-%m-%d")
            curator.add_songs_for_date(today)
        elif choice == '3':
            next_date = curator.find_next_unaccounted_date()
            print(f"Next unaccounted date: {next_date}")
            proceed = input(f"Add songs for {next_date}? (y/n): ").lower()
            if proceed == 'y':
                curator.add_songs_for_date(next_date)
        elif choice == '4':
            curator.show_curated_songs()
        elif choice == '5':
            date = input("Enter date (YYYY-MM-DD) or press Enter for latest: ")
            if date:
                curator.suggest_theme(date)
            else:
                curator.suggest_theme()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()