function toggleOverlay(event) {
    const overlayName = event.target.getAttribute('data-overlay') || event.target.closest('[data-overlay]').getAttribute('data-overlay');
    const overlay = document.querySelector(`#${overlayName}`);
    overlay.classList.toggle("hidden")
}

// Close any open overlay on press of escape key
document.addEventListener("keydown", (event) => {
    if (event.key == "Escape") {
        document.querySelectorAll(".overlay-background:not(.hidden)").forEach(overlay => {overlay.classList.add("hidden")});
    }
});