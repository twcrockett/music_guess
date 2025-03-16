import json
import difflib
import re
from collections import defaultdict


def normalize_title(title):
    """Normalize a title by removing common variations and punctuation."""
    # Convert to lowercase
    title = title.lower()

    # Remove anything in parentheses
    title = re.sub(r'\(.*?\)', '', title)

    # Remove common variations
    title = re.sub(r'remix|version|remaster|edit|radio|extended|feat\.|\bft\.|\bfeaturing\b', '', title)

    # Remove punctuation and extra spaces
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()

    return title


def normalize_artist(artist):
    """Normalize artist names."""
    # Convert to lowercase
    artist = artist.lower()

    # Remove featured artists
    artist = re.sub(r'ft\..*$|feat\..*$', '', artist)

    # Remove punctuation and extra spaces
    artist = re.sub(r'\s+', ' ', artist).strip()

    return artist


def remove_exact_duplicates(songs_list):
    """Remove exact duplicates based on title and artist."""
    unique_songs = {}

    for song in songs_list:
        # Create a key for each song
        key = f"{song['title'].lower()}|{song['artist'].lower()}"

        # If this song hasn't been seen before, add it to our unique songs
        if key not in unique_songs:
            unique_songs[key] = song

    return list(unique_songs.values())


def find_near_duplicates(songs_list):
    """Find songs that are likely duplicates but with slight variations."""
    # Group songs by normalized title
    title_groups = defaultdict(list)

    for song in songs_list:
        norm_title = normalize_title(song['title'])
        if len(norm_title) > 3:  # Skip very short titles
            title_groups[norm_title].append(song)

    # Find groups with multiple songs
    potential_duplicates = []

    for norm_title, songs in title_groups.items():
        if len(songs) > 1:
            # Check if artists are similar
            for i, song1 in enumerate(songs):
                norm_artist1 = normalize_artist(song1['artist'])

                for song2 in songs[i + 1:]:
                    norm_artist2 = normalize_artist(song2['artist'])

                    # Check if artists are similar
                    similarity = difflib.SequenceMatcher(None, norm_artist1, norm_artist2).ratio()

                    if similarity > 0.6 or norm_artist1 in norm_artist2 or norm_artist2 in norm_artist1:
                        potential_duplicates.append((song1, song2))

    return potential_duplicates


def recommend_songs_to_keep(songs_list):
    """Remove exact duplicates and suggest which near-duplicates to keep."""
    # First, remove exact duplicates
    unique_songs = remove_exact_duplicates(songs_list)
    print(f"Original song count: {len(songs_list)}")
    print(f"After removing exact duplicates: {len(unique_songs)}")
    print(f"Removed {len(songs_list) - len(unique_songs)} exact duplicates\n")

    # Now find near-duplicates
    near_duplicates = find_near_duplicates(unique_songs)

    if near_duplicates:
        print(f"Found {len(near_duplicates)} sets of near-duplicate songs:")

        # Track songs to remove
        songs_to_remove = set()

        for i, (song1, song2) in enumerate(near_duplicates):
            print(f"\nNear-duplicate set #{i + 1}:")
            print(f"  1. '{song1['title']}' by {song1['artist']} ({song1['year']})")
            print(f"  2. '{song2['title']}' by {song2['artist']} ({song2['year']})")

            # Simple heuristic: keep the original version if years differ significantly
            if abs(song1['year'] - song2['year']) > 5:
                keep_song = song1 if song1['year'] < song2['year'] else song2
                remove_song = song2 if song1['year'] < song2['year'] else song1
                print(f"  Recommendation: Keep the {keep_song['year']} version")
                songs_to_remove.add(id(remove_song))
            # If one has "Remix" in the title, prefer the original
            elif "remix" in song1['title'].lower() and "remix" not in song2['title'].lower():
                print(f"  Recommendation: Keep the original version (song 2)")
                songs_to_remove.add(id(song1))
            elif "remix" in song2['title'].lower() and "remix" not in song1['title'].lower():
                print(f"  Recommendation: Keep the original version (song 1)")
                songs_to_remove.add(id(song2))
            else:
                print(f"  Recommendation: Manual review needed")

        # Remove the recommended songs
        final_songs = [song for song in unique_songs if id(song) not in songs_to_remove]

        print(f"\nAfter near-duplicate recommendations: {len(final_songs)} songs")
        print(f"Recommended removing an additional {len(unique_songs) - len(final_songs)} near-duplicates")

        return final_songs
    else:
        print("No near-duplicates found.")
        return unique_songs


def analyze_decade_distribution(songs_list):
    """Analyze the distribution of songs by decade."""
    decade_counts = defaultdict(int)

    for song in songs_list:
        decade = (song['year'] // 10) * 10
        decade_counts[decade] += 1

    print("\nSong distribution by decade:")
    for decade in sorted(decade_counts.keys()):
        percentage = (decade_counts[decade] / len(songs_list)) * 100
        print(f"{decade}s: {decade_counts[decade]} songs ({percentage:.1f}%)")


def analyze_artist_frequency(songs_list):
    """Analyze the frequency of artists in the collection."""
    artist_counts = defaultdict(int)

    for song in songs_list:
        # Extract primary artist
        artist = song['artist'].split("ft.")[0].split("feat.")[0].strip()
        artist_counts[artist] += 1

    # Find top artists
    top_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    print("\nTop 20 artists by number of songs:")
    for i, (artist, count) in enumerate(top_artists):
        print(f"{i + 1}. {artist}: {count} songs")


def main():
    # Load the songs from the JSON file
    with open('songs.json', 'r', encoding='utf-8') as f:
        songs = json.load(f)

    # Process the songs
    final_songs = recommend_songs_to_keep(songs)

    # Analyze the cleaned dataset
    analyze_decade_distribution(final_songs)
    analyze_artist_frequency(final_songs)

    # Save the results
    with open('cleaned_songs.json', 'w', encoding='utf-8') as f:
        json.dump(final_songs, f, ensure_ascii=False, indent=2)

    print(f"\nCleaned songs saved to cleaned_songs.json")


if __name__ == "__main__":
    main()