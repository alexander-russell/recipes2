// Create event listener to form submission, needs to be redone each time the diary is replaced
function registerInputListeners() {
    document.getElementById("diary-input").addEventListener('keydown', (event) => {
        if (event.key == "Enter") {
            event.preventDefault();
            submitNewDiaryEntry()
        }
    })
}

// Submits a post request and replaces the diary using the JSON response
function submitNewDiaryEntry() {
    const content = document.getElementById("diary-input").innerText;
    const endpoint = `${window.location.pathname}/diary/add`

    fetch(endpoint, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector("meta[name='csrf-token']").content,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `content=${encodeURIComponent(content)}`
    })
        .then(response => response.json())
        .then(data => {
            // Saves and preserves scroll, replaces diary, sets it to visible, clears input
            const scrollPos = document.querySelector(".recipe-diary").scrollTop;
            document.getElementById("diary-overlay").outerHTML = data.html;
            document.getElementById("diary-overlay").classList.remove("hidden")
            document.getElementById("diary-input").innerText = "";
            document.querySelector(".recipe-diary").scrollTop = scrollPos
            registerInputListeners()
        })
        .catch((error) => console.error("Error:", error));
}

// Configure event listener for input span enter keypress
registerInputListeners()

// Update timestamp next to input every 20 seconds
setInterval(() => {
    document.getElementById("diary-current-time").textContent = new Date().toLocaleTimeString('eo', { hour12: false }).substring(0, 5)
}, 20000)
