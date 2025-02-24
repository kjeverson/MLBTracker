$(document).ready(function() {
    fetch('/api/players/', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        let html = "";
        data.forEach(player => {
            document.querySelector("#playerListBody").appendChild(createPlayerRow(player));
        });
    })
    .finally(() => {
        activateSearchBar();
        activatePositionSelector();
    })
    .catch(error => {
        console.error('Error:', error);
    })
});

function getSelectedPosition(){
    var button = document.querySelector("#playerPositionSelector .btn:disabled");
    return button.getAttribute("data-pos");
}

function clearSelected(buttons){
    buttons.forEach(button => {
        button.disabled = false;
    })
}

function activatePositionSelector(){
    var buttons = document.querySelectorAll("#playerPositionSelector .btn");

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            clearSelected(buttons);
            this.disabled = true;
            const filterPosition = this.getAttribute("data-pos");

            var table = document.getElementById("playerListBody");
            if(filterPosition === 'ALL') {
                for (let row of table.rows) {
                    if(row.getAttribute("hidden")) {
                        row.removeAttribute("hidden");
                    }
                }
            }
            else {
                for (let row of table.rows) {
                    let position = row.getAttribute("data-pos");
                    if (row.getAttribute("hidden")) {
                        row.removeAttribute("hidden");
                    }
                    if (!filterPosition.includes(position)) {
                        row.setAttribute("hidden", "hidden");
                    }
                }
            }
        });
    });
}

function activateSearchBar(){
    var search = document.getElementById("playerSearchBar");
    search.addEventListener("input", (e) => {
        var table = document.getElementById("playerListBody");
        let searchValue = e.target.value.toLowerCase();
        let position = getSelectedPosition();
        for (let row of table.rows) {
            let name = row.getAttribute("data-name");
            if (position.includes(row.getAttribute("data-pos")) || position === 'ALL' && row.getAttribute("hidden")) {
                row.removeAttribute("hidden");
            }
            if (!name.includes(searchValue)) {
                row.setAttribute("hidden", "hidden");
            }
        }
    })
}

function createPlayerRow(player) {
    const tr = document.createElement("tr");
    tr.classList.add("p-0", "m-0");
    tr.dataset.name = `${player.name_full}`.toLowerCase();
    if(player.secondary_position) {
        tr.dataset.pos = `${player.primary_position}, ${player.secondary_position}`;
    }
    else {
        tr.dataset.pos = `${player.primary_position}`;
    }

    const td = document.createElement("td");
    td.classList.add("p-0", "m-0");
    td.style.background = `linear-gradient(to right, ${player.team.primary_color} 15%, rgba(0,0,0,0) 65%)`;

    const rowDiv = document.createElement("div");
    rowDiv.classList.add("row", "align-items-center", "player-table-row");
    rowDiv.style.overflow = "hidden";

    const teamLogoContainer = document.createElement("div");
    teamLogoContainer.classList.add("ptr-team-logo-container");

    const teamLogo = document.createElement("img");
    teamLogo.src = `${teamLogoPath}${player.team.id}.png`
    teamLogo.alt = "Team Logo";
    teamLogo.classList.add("ptr-team-logo");

    teamLogoContainer.appendChild(teamLogo);

    const emptyCol = document.createElement("div");
    emptyCol.classList.add("col-2", "text-center");

    const playerInfoCol = document.createElement("div");
    playerInfoCol.classList.add("col-9", "pb-2");
    playerInfoCol.style.position = "relative";

    const playerName = document.createElement("h6");
    playerName.style.textTransform = "uppercase";
    playerName.style.marginBottom = "0";
    playerName.innerHTML = `<i>${player.name_full}</i>`;

    const playerDetails = document.createElement("small");
    playerDetails.style.fontWeight = "200";
    playerDetails.style.textTransform = "uppercase";
    playerDetails.style.marginTop = "0";

    const positionBadge = document.createElement("span");
    positionBadge.classList.add("badge", "bg-light", "text-dark");
    if(player.secondary_position){
        positionBadge.textContent = player.get_primary_position + "/" + player.get_secondary_position;
    }
    else {
        positionBadge.textContent = player.get_primary_position;
    }

    playerDetails.appendChild(positionBadge);
    playerDetails.appendChild(document.createTextNode(` ${player.team.full_name}`));

    playerInfoCol.appendChild(playerName);
    playerInfoCol.appendChild(playerDetails);

    const clipboardCol = document.createElement("div");
    clipboardCol.classList.add("col-1", "text-center");

    const clipboardIcon = document.createElement("i");

    clipboardIcon.addEventListener("mouseenter", () => {
        clipboardIcon.style.cursor = "pointer"; // Hand cursor
    });

    clipboardIcon.addEventListener("mouseleave", () => {
        clipboardIcon.style.cursor = "default"; // Reset cursor
    });

    clipboardIcon.classList.add("bi", "bi-clipboard2-data-fill", "h4");
    clipboardIcon.type = "button";
    clipboardIcon.dataset.playerId = `${player.id}`;
    clipboardIcon.addEventListener('click', function () {
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
    clipboardCol.appendChild(clipboardIcon);

    rowDiv.appendChild(teamLogoContainer);
    rowDiv.appendChild(emptyCol);
    rowDiv.appendChild(playerInfoCol);
    rowDiv.appendChild(clipboardCol);

    td.appendChild(rowDiv);
    tr.appendChild(td);

    return tr;
}