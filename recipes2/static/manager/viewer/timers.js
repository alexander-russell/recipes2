// Get timers, add event listeners for start/stop and reset
const timers = document.querySelectorAll(".timer")
setInterval(timekeeper, 1000);

// Register event listeners
for (const timer of timers) {
    timer.addEventListener("click", toggleTimer)
    timer.addEventListener("dblclick", resetTimer)
}

// Handle timer state
function toggleTimer(event) {
    const timer = event.currentTarget
    if (!timer.classList.contains("active")) {
        // Start timer
        timer.classList.add("active");
        timer.setAttribute("started", Date.now());
    } else if (timer.classList.contains("elapsed")) {
        // Reset the timer
        resetTimer({ currentTarget: timer });
    } else {
        // Stop timer
        timer.classList.remove("active");
        const runtime = Date.now() - timer.getAttribute("started");
        const remaining = 0 + timer.getAttribute("remaining") - (runtime / 1000)
        timer.setAttribute("remaining", remaining);
    }
}

// Handle timer reset
function resetTimer(event) {
    const timer = event.currentTarget
    timer.querySelector(".timer-time").textContent = formatTime(timer.getAttribute("total"));
    timer.setAttribute("remaining", timer.getAttribute("total"));
    timer.classList.remove("active", "elapsed", "flashing");
}

function hideTimers() {
    document.querySelector(".timers").classList.add("hidden")
    document.querySelector("li:has(title[id='clock-icon'])").classList.remove("hidden")
}

function showTimers() {
    document.querySelector(".timers").classList.remove("hidden")
    document.querySelector("li:has(title[id='clock-icon'])").classList.add("hidden")
}

function formatTime(seconds) {
    const SECONDS_PER_HOUR = 3600
    if (seconds >= SECONDS_PER_HOUR) {
        startIdx = 12
    } else {
        startIdx = 14
    }
    return new Date(seconds * 1000).toISOString().slice(startIdx, 19);
}

// Update active timers or clock
function timekeeper() {
    // Update active timers
    document.querySelectorAll('.timer.active').forEach(timer => {
        // Calculate remaining time
        const runtime = Date.now() - timer.getAttribute("started");
        const remaining = 0 + timer.getAttribute("remaining") - (runtime / 1000);

        timer.querySelector(".timer-time").textContent = formatTime(remaining > 0 ? remaining : -remaining);

        if (remaining <= 0) {
            timer.classList.add("elapsed");
            timer.classList.toggle("flashing");

            //Speak timer name aloud
            if (!timer.classList.contains("speaking")) {
                //Add speaking class (so too many utterances aren't queued)
                timer.classList.add("speaking");

                //Arrange text to speech of timer name
                const speaker = window.speechSynthesis
                const utterance = new SpeechSynthesisUtterance(timer.getAttribute("name"));
                speaker.speak(utterance);

                //Remove speaking class when this is done
                utterance.addEventListener("end", () => {
                    timer.classList.remove("speaking");
                });
            }
        }
    });

    // Update clock if exists
    const clock = document.querySelector(".clock")
    if (clock) {
        clock.textContent = new Date().toTimeString().substring(0, 8);
    }
}