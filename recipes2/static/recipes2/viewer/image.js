function selectImageByIndex(index) {
    const thumbnails = Array.from(document.querySelectorAll('.thumbnail-strip img'));
    if (index < 0 || index >= thumbnails.length) return;

    const newSelected = thumbnails[index];
    updateSelectedImage(newSelected);
}

function updateSelectedImage(imageElement) {
    if (!imageElement) return;

    // Update main image src and alt
    const mainImage = document.getElementById('main-image');
    mainImage.src = imageElement.dataset.fullSrc || imageElement.src;
    mainImage.alt = imageElement.alt;

    // Update thumbnail selection
    const thumbnails = imageElement.parentNode.querySelectorAll('img');
    thumbnails.forEach(img => img.classList.remove('selected'));
    imageElement.classList.add('selected');
}

function selectImage(event) {
    const clicked = event.target;
    if (clicked.tagName !== 'IMG') return;
    updateSelectedImage(clicked);
}

function moveToNextImage() {
    console.log('Moving to next image');
    const thumbnails = Array.from(document.querySelectorAll('.thumbnail-strip img'));
    const currentIndex = thumbnails.findIndex(img => img.classList.contains('selected'));
    if (currentIndex === -1) return;
    const nextIndex = (currentIndex + 1) % thumbnails.length;
    selectImageByIndex(nextIndex);
}

function moveToPreviousImage() {
    console.log('Moving to previous image');
    const thumbnails = Array.from(document.querySelectorAll('.thumbnail-strip img'));
    const currentIndex = thumbnails.findIndex(img => img.classList.contains('selected'));
    if (currentIndex === -1) return;
    const prevIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
    selectImageByIndex(prevIndex);
}

// Keyboard navigation listener
document.addEventListener('keydown', function (event) {
    console.log('Key pressed:', event.key);
    const imageOverlay = document.querySelector('#image-overlay');
    if (imageOverlay && !imageOverlay.classList.contains('hidden')) {
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            event.preventDefault();
            moveToNextImage();
        } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            event.preventDefault();
            moveToPreviousImage();
        }
    };
});
