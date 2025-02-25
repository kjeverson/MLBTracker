document.addEventListener("DOMContentLoaded", () => {
    const currentPage = window.location.pathname;
    if(currentPage == '/batting/'){
        fetchBattingStats();
    }
    else {
        fetchPitchingStats();
    }

});

function displayBattingStats(stats) {
    return new Promise((resolve, reject) => {
        const tableBody = document.getElementById("statsTableBody");
        tableBody.innerHTML = ""; // Clear previous data

        stats.forEach(stat => {

            if(stat.team != 'OVR') {
                const row = document.createElement("tr");
                const teamImage = `/static/img/MLB/${stat.team}.png`;

                row.dataset.playerId = `${stat.player.id}`;

                row.innerHTML = `
                    <td>${stat.player.name_short}</td>
                    <td>${stat.player.get_primary_position}</td>
                    <td><img src="${teamImage}" height="20px"> ${stat.team}</td>
                    <td>${stat.league}</td>
                    <td>${stat.games}</td>
                    <td>${stat.at_bats}</td>
                    <td>${stat.runs}</td>
                    <td>${stat.hits}</td>
                    <td>${stat.doubles}</td>
                    <td>${stat.triples}</td>
                    <td>${stat.home_runs}</td>
                    <td>${stat.bases_on_balls}</td>
                    <td>${stat.strikeouts}</td>
                    <td>${stat.batting_average}</td>
                    <td>${stat.slugging_percentage}</td>
                    <td>${stat.batting_balls_in_play}</td>
                `;

                row.addEventListener('click', function () {
                const playerId = this.getAttribute('data-player-id');

                fetch(`/get-player-modal/${playerId}/`)
                    .then(response => response.json())
                    .then(data => {
                        const existingModal = document.getElementById('playerModal');
                        if (existingModal) {
                            existingModal.remove();
                        }
                        document.body.insertAdjacentHTML('beforeend', data.html);
                        const modal = new bootstrap.Modal(document.getElementById('playerModal'));
                        modal.show();
                    })
                    .catch(error => console.error('Error:', error));
                });

                tableBody.appendChild(row);
            }
        });
        resolve();
    });
}

function fetchBattingStats() {
    const year = document.getElementById("yearSelect").value;
    const url = `/api/batting-stats/${year}/`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if ($.fn.DataTable.isDataTable('#statsTable')) {
                $('#statsTable').DataTable().clear().destroy();
            }

            displayBattingStats(data);
        })
        .then(() => {
            $('#statsTable').DataTable({
                "searching": false,
                "paging": false,
                "info": false
            });
        })
        .catch(error => {
            console.error("Error fetching batting stats:", error);
        });
}

function displayPitchingStats(stats) {
    return new Promise((resolve, reject) => {
        const tableBody = document.getElementById("statsTableBody");
        tableBody.innerHTML = "";

        stats.forEach(stat => {

            if(stat.team != 'OVR') {
                const row = document.createElement("tr");
                const teamImage = `/static/img/MLB/${stat.team}.png`;

                row.dataset.playerId = `${stat.player.id}`;

                row.innerHTML = `
                    <td>${stat.player.name_short}</td>
                    <td>${stat.player.get_primary_position}</td>
                    <td><img src="${teamImage}" height="20px"> ${stat.team}</td>
                    <td>${stat.league}</td>
                    <td>${stat.games}</td>
                    <td>${stat.games_started}</td>
                    <td>${stat.wins}</td>
                    <td>${stat.losses}</td>
                    <td>${stat.win_percentage}</td>
                    <td>${stat.innings_pitched}</td>
                    <td>${stat.strikeouts}</td>
                    <td>${stat.bases_on_balls}</td>
                    <td>${stat.hits}</td>
                    <td>${stat.saves}</td>
                    <td>${stat.batting_average}</td>
                    <td>${stat.whip}</td>
                    <td>${stat.k9}</td>
                    <td>${stat.bb9}</td>
                `;

                row.addEventListener('click', function () {
                const playerId = this.getAttribute('data-player-id');

                fetch(`/get-player-modal/${playerId}/`)
                    .then(response => response.json())
                    .then(data => {
                        const existingModal = document.getElementById('playerModal');
                        if (existingModal) {
                            existingModal.remove();
                        }
                        document.body.insertAdjacentHTML('beforeend', data.html);
                        const modal = new bootstrap.Modal(document.getElementById('playerModal'));
                        modal.show();
                    })
                    .catch(error => console.error('Error:', error));
                });

                tableBody.appendChild(row);
            }
        });
        resolve();
    });
}

function fetchPitchingStats() {
    const year = document.getElementById("yearSelect").value;
    const url = `/api/pitching-stats/${year}/`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if ($.fn.DataTable.isDataTable('#statsTable')) {
                $('#statsTable').DataTable().clear().destroy();
            }

            displayPitchingStats(data);
        })
        .then(() => {
            $('#statsTable').DataTable({
                "searching": false,
                "paging": false,
                "info": false
            });
        })
        .catch(error => {
            console.error("Error fetching pitching stats:", error);
        });
}