function toggleOverlay(event) {
    const overlayName = event.target.getAttribute('data-overlay') || event.target.closest('[data-overlay]').getAttribute('data-overlay');
    const overlay = document.querySelector(`#${overlayName}`);
    overlay.classList.toggle("hidden")
}