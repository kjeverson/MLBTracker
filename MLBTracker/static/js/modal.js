
function toggleStats(isPitching) {
    var pitchingButton = document.getElementById("pitchingBtn");
    var battingButton = document.getElementById("battingBtn");
    var pitchingStats = document.getElementById("modalPitchingStats");
    var battingStats = document.getElementById("modalBattingStats");

    if (isPitching) {
        pitchingButton.disabled = true;
        battingButton.disabled = false;
        pitchingStats.classList.remove("visually-hidden");
        battingStats.classList.add("visually-hidden");
    } else {
        pitchingButton.disabled = false;
        battingButton.disabled = true;
        pitchingStats.classList.add("visually-hidden");
        battingStats.classList.remove("visually-hidden");
    }
}