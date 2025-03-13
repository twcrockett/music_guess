# [Yearworm](https://music-guess-bynw.onrender.com/) <img alt="" height="60" src="https://github.com/twcrockett/song-guess-game/assets/logo.png"/>


A web game that challenges players to guess the release year of popular songs. Play daily challenges or practice in free play mode!


## The Game

- **Daily Challenge**: 5 rounds of curated songs that change each day. Everyone gets the same songs for fair competition.
- **Free Play Mode**: Practice with as many songs as you like, with customizable options.
- **Scoring System**: Start with 100 points and lose points over based on how far off your guesses are.

## How to Play

1. Choose a game mode (Daily Challenge or Free Play)
2. Listen to the song preview
3. Guess the year the song was released
4. Get feedback on how close your guess was
5. Try to maintain a high score!

## The Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, and vanilla JavaScript
- **Audio**: Uses iTunes API to fetch song previews
- **Deployment**: Hosted on Render

## Local Development

1. Clone the repository:
   ```
   git clone https://github.com/twcrockett/song-guess-game.git
   cd song-guess-game
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```
   python app.py
   ```

5. Open http://localhost:5000 in your browser

## Deployment

This application is deployed on Render. The deployment automatically picks up changes pushed to the main branch.

## Data Management

This will eventually change when I figure some metadata stuff out!

- `songs.json`: Contains the main database of songs
- `curated_songs.json`: Contains daily curated song lists

## Credits

- Created poorly by [Tay](https://twcrockett.github.io/)
- Uses iTunes API for song previews

## License

MIT

---

Visit the live game [here](https://music-guess-bynw.onrender.com/)