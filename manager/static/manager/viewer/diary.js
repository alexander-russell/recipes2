// Updatee CSRF token from user
async function refreshCSRFToken() {
    return fetch('/yum/csrf/') //TODO use a better url here
        .then(response => { if (response.ok) { return response.json() } else { return Promise.reject("") } })
        .then(data => {
            const meta = document.querySelector("meta[name='csrf-token']");
            if (meta) {
                meta.content = data.csrfToken;
            }
        })
        .catch((error) => { });
}

// Create event listener to form submission, needs to be redone each time the diary is replaced
function registerInputListeners() {
    document.getElementById("diary-input").addEventListener('keydown', (event) => {
        if (event.key == "Enter") {
            event.preventDefault();
            refreshCSRFToken()
                .then(submitNewDiaryEntry);
        }
    })

    // When input has no text, make sure it is properly empty so css :empty works
    document.getElementById("diary-input").addEventListener('input', (event) => {
        if (event.target.textContent == "") {
            event.target.innerHTML = "";
        }
    })
}

// Submits a post request and replaces the diary using the JSON response
function submitNewDiaryEntry() {
    const content = document.getElementById("diary-input").innerText;
    const endpoint = `${window.location.pathname}diary/add/`

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
            if (!data.success && data.reason == "lackspermission") {
                document.querySelector("#diary-add-login-tip").classList.remove("hidden");
                return
            } else {
                // Saves and preserves scroll, hides login tip, replaces diary, sets it to visible, clears input
                document.querySelector("#diary-add-login-tip").classList.add("hidden");
                const scrollPos = document.querySelector(".recipe-diary").scrollTop;
                document.getElementById("diary-overlay").outerHTML = data.html;
                document.getElementById("diary-overlay").classList.remove("hidden")
                document.getElementById("diary-input").innerText = "";
                document.querySelector(".recipe-diary").scrollTop = scrollPos
                registerInputListeners()
            }
        })
        .catch((error) => console.error("Error:", error));
}

// Configure event listener for input span enter keypress
registerInputListeners()

// Update timestamp next to input every 20 seconds
setInterval(() => {
    document.getElementById("diary-current-time").textContent = new Date().toLocaleTimeString('eo', { hour12: false }).substring(0, 5)
}, 20000)
