/**
 * Common JavaScript functions
 */

// Navbar HTML template
const navbarHTML = `
<nav class="navbar">
    <div class="navbar-container">
        <a href="/" class="navbar-logo">Guess the Song Year</a>
        <ul class="navbar-menu">
            <li><a href="/" class="navbar-item">Home</a></li>
            <li><a href="/daily" class="navbar-item">Daily Challenge</a></li>
            <li><a href="/free_options" class="navbar-item">Free Play</a></li>
        </ul>
    </div>
</nav>
`;

// Function to inject navbar
function injectNavbar() {
    // Get the body element
    const body = document.body;

    // Insert the navbar at the beginning of the body
    body.insertAdjacentHTML('afterbegin', navbarHTML);

    // Highlight current page in navbar
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.navbar-item');

    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (currentPath === href ||
            (href !== '/' && currentPath.startsWith(href))) {
            item.classList.add('active');
        }
    });
}

// Helper function to format a song's year response
function formatYearDifferenceFeedback(yearDifference, actualYear, isCorrect) {
    if (isCorrect) {
        return 'Perfect! You guessed the exact year!';
    } else {
        return `Off by ${yearDifference} years. The actual year was ${actualYear}.`;
    }
}

// Helper function to generate game over message based on score
function generateGameOverMessage(score) {
    if (score >= 90) {
        return 'Amazing! You\'re a music history expert!';
    } else if (score >= 70) {
        return 'Great job! You really know your music!';
    } else if (score >= 50) {
        return 'Not bad! You have a decent knowledge of music history.';
    } else {
        return 'Better luck next time! Keep listening to more music!';
    }
}

// Helper function to validate year input
function validateYearInput(year) {
    const currentYear = new Date().getFullYear();
    if (isNaN(year) || year < 1900 || year > currentYear) {
        return {
            valid: false,
            message: `Please enter a valid year between 1900 and ${currentYear}`
        };
    }
    return { valid: true };
}

// Helper function to set up audio player with guessing form
function setupAudioPlayer(container, previewUrl, title = null) {
    if (previewUrl) {
        // No title in the player display
        container.innerHTML = `
            <div class="audio-player">
                <p>🎵 Now Playing...</p>
                <audio id="song-audio" preload="auto" controls>
                    <source src="${previewUrl}" type="audio/mp4">
                    Your browser does not support the audio element.
                </audio>
                <div class="guess-form">
                    <input type="number" id="year-guess" placeholder="Enter year (e.g., 1985)" min="1900" max="2024">
                    <button id="guess-btn" type="button">Guess</button>
                    <button id="skip-btn" type="button">Skip</button>
                </div>
            </div>
        `;

        // Get the audio element
        const audio = document.getElementById('song-audio');

        // Set autoplay after a slight delay to avoid some browser issues
        setTimeout(() => {
            try {
                audio.play().catch(e => console.log("Autoplay prevented: ", e));
            } catch (err) {
                console.log("Error autoplaying: ", err);
            }
        }, 500);

        return true;
    } else {
        // Fallback message if no preview
        container.innerHTML = `
            <div class="audio-player">
                <p>Audio preview not available for this song</p>
                <div class="guess-form">
                    <input type="number" id="year-guess" placeholder="Enter year (e.g., 1985)" min="1900" max="2024">
                    <button id="guess-btn" type="button">Guess</button>
                    <button id="skip-btn" type="button">Skip</button>
                </div>
            </div>
        `;

        return false;
    }
}

// Add event listener for enter key on year input
function setupEnterKeyForGuess(inputElement, buttonElement) {
    inputElement.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            buttonElement.click();
        }
    });
}

// Common footer HTML
const footerHTML = `
<footer>
       <p>Created by Big Tay | <a href="https://github.com/twcrockett/song-guess-game" target="_blank">GitHub</a></p>
</footer>
`;