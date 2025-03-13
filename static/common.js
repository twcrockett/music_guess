/**
 * Common JavaScript functions
 */

// Navbar HTML template
const navbarHTML = `
<nav class="navbar">
    <div class="navbar-container">
        <a href="/" class="navbar-logo">
            <img src="/static/logo.png" alt="Yearworm Logo" class="navbar-logo-img">
            Yearworm
        </a>
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
        return 'Perfect! You guessed the exact year! 🎯';
    } else {
        return `Off by ${yearDifference} years. The actual year was ${actualYear}. ${yearDifference <= 5 ? 'So close!' : ''}`;
    }
}

// Helper function to generate game over message based on score
function generateGameOverMessage(score) {
    // Arrays of music references for each score range
    const expertMessages = [
        "Sweet Child O' Mine! You're a bona fide rock historian! 🎸",
        "You've got the Knowledge, just like Lauryn Hill! 🏆",
        "You'll never be 'Rick Rolled' with knowledge like that! 🎤",
        "Don't Stop Believin' in your music expertise! 🌟",
        "You must have Spotify on 24/7! That was Dynamite! 💯",
        "You've got all the Uptown Funk you need! 🎵",
        "Another One Bites The Dust! You crushed this quiz! 👑"
    ];

    const goodMessages = [
        "You can't always get what you want, but you got most of these right! 🎵",
        "You've got rhythm, you've got music, you've got most answers correct! 🎧",
        "Hit me baby one more time... with another quiz please! 🎤",
        "We Will, We Will, Rock You... with a slightly harder quiz next time! 👏",
        "You're walking on sunshine with that performance! ☀️",
        "Not quite a Smooth Criminal of music knowledge, but close! 🕴️",
        "You know more than most! It must be all that Rhythm Nation training. 🔥",
        "That's The Way (Uh-Huh, Uh-Huh) we like your answers! 👍",
        "Your music knowledge is a Thriller, a Thriller night! 🌙"
    ];

    const averageMessages = [
        "Don't cry for me, Argentina—your score is actually decent! 🎭",
        "Every Rose Has Its Thorn, and every quiz taker misses some questions! 🌹",
        "With A Little Help From My Friends, you might score higher next time! 👫",
        "You're not bad, but maybe a little Comfortably Numb on some questions. 💊",
        "Don't Stop 'Til You Get Enough... correct answers, that is! 🕺",
        "Like Britney says, 'Oops!... I Did It' okay on this quiz! 😅",
        "We Can Work It Out with a little more studying! 📚",
        "You took the midnight train going... somewhere in the middle! 🚆",
        "More than a feeling, you've got some music knowledge brewing! 🎸"
    ];

    const needsWorkMessages = [
        "Yesterday, all your troubles seemed so far away, but today it seems they're here to stay. 🎹",
        "Bye Bye Bye to your bragging rights. 👋",
        "Livin' On A Prayer with some of those guesses, weren't you? 🙏",
        "You might need some R-E-S-P-E-C-T for the artists you're listening to! 🎵",
        "Here, <a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ'>this</a> might help you improve for next time. 🎧",
        "Sweet Dreams are made of... better scores than this! Keep trying! 💤"
    ];

    // Select a random message based on score
    let messagePool;
    if (score >= 90) {
        messagePool = expertMessages;
    } else if (score >= 70) {
        messagePool = goodMessages;
    } else if (score >= 50) {
        messagePool = averageMessages;
    } else {
        messagePool = needsWorkMessages;
    }

    // Pick a random message from the appropriate pool
    const randomIndex = Math.floor(Math.random() * messagePool.length);
    return messagePool[randomIndex];
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

// Helper function to set up audio player with guessing form (improved version)
function setupAudioPlayerNew(container, previewUrl) {
    if (previewUrl) {
        // More streamlined player without "Now Playing" text
        container.innerHTML = `
            <div class="audio-player">
                <audio id="song-audio" preload="auto" controlsList="nodownload nospeed" controls>
                    <source src="${previewUrl}" type="audio/mp4">
                    Your browser does not support the audio element.
                </audio>
                <div class="guess-form">
                    <input type="number" id="year-guess" placeholder="Enter year" min="1900" max="2024">
                    <div class="button-group">
                        <button id="guess-btn" type="button">Guess</button>
                        <button id="skip-btn" type="button">Skip</button>
                    </div>
                </div>
            </div>
        `;

        // Get the audio element
        const audio = document.getElementById('song-audio');

        // Set initial volume from localStorage or use default 0.5 (50%)
        const savedVolume = localStorage.getItem('yearworm_volume');
        audio.volume = savedVolume !== null ? parseFloat(savedVolume) : 0.5;

        // Save volume preference when user adjusts it
        audio.addEventListener('volumechange', function() {
            localStorage.setItem('yearworm_volume', audio.volume);
        });

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
                    <div class="button-group">
                        <button id="guess-btn" type="button">Guess</button>
                        <button id="skip-btn" type="button">Skip</button>
                    </div>
                </div>
            </div>
        `;

        return false;
    }
}

// Keep the old function for backward compatibility
function setupAudioPlayer(container, previewUrl, title = null) {
    return setupAudioPlayerNew(container, previewUrl);
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

// Helper function to show the next button
function showNextButton(nextBtnElement) {
    if (nextBtnElement) {
        nextBtnElement.style.display = 'flex';
        nextBtnElement.classList.add('visible');
    }
}

/**
 * Initialize the score circle by replacing the current score display
 * @param {string} containerId - ID of the container element
 * @param {string} scoreId - ID of the score span element
 * @param {string} label - Label to show (e.g., "Score" or "Avg")
 * @param {boolean} isAverage - Whether this is an average score (changes styling)
 */
function initScoreCircle(containerId, scoreId, label = "Score", isAverage = false) {
    const container = document.getElementById(containerId);
    const scoreSpan = document.getElementById(scoreId);

    if (!container || !scoreSpan) return;

    // Get the current score value
    const currentValue = scoreSpan.textContent;

    // Ensure container is using flex display
    container.style.display = 'flex';
    container.style.alignItems = 'center';
    container.style.gap = '12px';

    // Create the new structure - with label to the left of the circle
    const circleHtml = `
        <span class="score-label">${label}:</span>
        <div class="score-circle ${isAverage ? 'avg-score' : ''}">
            <span class="score-value score-transition" id="${scoreId}">${currentValue}</span>
        </div>
    `;

    // Replace the container contents
    container.innerHTML = circleHtml;

    // Update circle class based on score
    updateScoreCircleClass(scoreId, parseFloat(currentValue), isAverage);
}

/**
 * Update the score and trigger animation
 * @param {string} scoreId - ID of the score span element
 * @param {number} newValue - New score value
 * @param {boolean} isAverage - Whether this is an average score
 */
function updateScoreWithAnimation(scoreId, newValue, isAverage = false) {
    const scoreSpan = document.getElementById(scoreId);
    if (!scoreSpan) return;

    const oldValue = parseFloat(scoreSpan.textContent);

    // Update the value
    scoreSpan.textContent = newValue;

    // Get parent circle
    const scoreCircle = scoreSpan.closest('.score-circle');
    if (!scoreCircle) return;

    // Add animation class
    scoreCircle.classList.add('score-change');

    // Update the circle class based on new value
    updateScoreCircleClass(scoreId, newValue, isAverage);

    // Remove animation class after animation completes
    setTimeout(() => {
        scoreCircle.classList.remove('score-change');
    }, 600);
}

/**
 * Update the score circle class based on value
 * @param {string} scoreId - ID of the score span element
 * @param {number} value - Score value
 * @param {boolean} isAverage - Whether this is an average score
 */
function updateScoreCircleClass(scoreId, value, isAverage = false) {
    const scoreSpan = document.getElementById(scoreId);
    if (!scoreSpan) return;

    const scoreCircle = scoreSpan.closest('.score-circle');
    if (!scoreCircle) return;

    // Remove existing classes
    scoreCircle.classList.remove('low-score', 'high-score');

    // Don't add color classes for average mode
    if (isAverage) return;

    // Add appropriate class based on score
    if (value < 50) {
        scoreCircle.classList.add('low-score');
    } else if (value >= 80) {
        scoreCircle.classList.add('high-score');
    }
}


// Common footer HTML
const footerHTML = `
<footer>
    <p><a href="https://twcrockett.github.io/" target="_blank"><img src="https://avatars.githubusercontent.com/u/79346208?v=4" class="footer-avatar" alt="Tay's avatar"></a> Made by Tay | <a href="https://github.com/twcrockett/yearworm" target="_blank">GitHub</a></p>
</footer>
`;