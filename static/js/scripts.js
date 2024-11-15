document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById('shuffle-wager-standings')) {
        updateShuffleWagerStandings();
    }
    if (document.getElementById('shuffle-raffle-standings')) {
        updateShuffleRaffleStandings();
    }
    if (document.getElementById('chicken-wager-standings')) {
        updateChickenStandings();
    }

    // Update all data every 15 minutes if enabled
    setInterval(function() {
        if (document.getElementById('shuffle-wager-standings')) {
            updateShuffleWagerStandings();
        }
        if (document.getElementById('shuffle-raffle-standings')) {
            updateShuffleRaffleStandings();
        }
        if (document.getElementById('chicken-wager-standings')) {
            updateChickenStandings();
        }
    }, 15 * 60 * 1000);
});

// Fetch and update Shuffle Wager standings
function updateShuffleWagerStandings() {
    fetch('/shuffle_data')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Shuffle Wager data:", data);
            const shuffleStandings = document.getElementById('shuffle-wager-standings');
            shuffleStandings.innerHTML = '';

            // Populate top 11 standings from fetched data
            for (const [key, value] of Object.entries(data.top_wagerers)) {
                shuffleStandings.innerHTML += `<div>${value.username}: ${value.wager}</div>`;
            }
        })
        .catch(error => console.error('Error fetching Shuffle wager data:', error));
}

// Fetch and update Shuffle Raffle standings
function updateShuffleRaffleStandings() {
    fetch('/shuffle_raffle_data')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Shuffle Raffle data:", data);
            const shuffleRaffleStandings = document.getElementById('shuffle-raffle-standings');
            shuffleRaffleStandings.innerHTML = '';

            // Populate ticket standings
            for (const [key, value] of Object.entries(data.top_tickets)) {
                shuffleRaffleStandings.innerHTML += `<div>${value.username}: ${value.tickets} tickets</div>`;
            }
        })
        .catch(error => console.error('Error fetching Shuffle raffle data:', error));
}

// Fetch and update Chicken.gg standings
function updateChickenStandings() {
    fetch('/chicken_data')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched Chicken data:", data);
            const chickenStandings = document.getElementById('chicken-wager-standings');
            chickenStandings.innerHTML = '';

            // Populate top 11 standings from fetched data
            for (const [key, value] of Object.entries(data)) {
                chickenStandings.innerHTML += `<div>${value.username}: ${value.wager}</div>`;
            }
        })
        .catch(error => console.error('Error fetching Chicken wager data:', error));
}
