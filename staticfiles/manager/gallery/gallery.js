document.addEventListener("DOMContentLoaded", () => {
  const gallery = document.getElementById("gallery");
  let position = 0;
  const speed = 1; // pixels per frame
  let animationId = null;

  // Clone enough items to fill at least twice the visible width for smooth looping
  function cloneItems() {
    const totalWidth = gallery.scrollWidth;
    const visibleWidth = gallery.offsetWidth;
    let widthAccum = totalWidth;

    let children = Array.from(gallery.children);
    let i = 0;

    // Keep cloning until total width is at least twice visible width
    while (widthAccum < visibleWidth * 2) {
      const clone = children[i].cloneNode(true);
      gallery.appendChild(clone);
      widthAccum += clone.offsetWidth;
      i = (i + 1) % children.length;
    }
  }

  // Start scrolling animation
  function startScrolling() {
    if (!animationId) {
      animationId = requestAnimationFrame(step);
    }
  }

  // Stop scrolling animation
  function stopScrolling() {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    }
  }

  // Animation step
  function step() {
    position -= speed;

    // If first child fully out of view, move it to the end and adjust position
    const firstChild = gallery.children[0];
    if (!firstChild) return;

    const firstChildWidth = firstChild.offsetWidth;

    if (-position >= firstChildWidth) {
      gallery.appendChild(firstChild);
      position += firstChildWidth;
    }

    gallery.style.transform = `translateX(${position}px)`;

    animationId = requestAnimationFrame(step);
  }

  // Initialize
  cloneItems();
  startScrolling();

  // Pause on hover
  gallery.addEventListener("mouseenter", stopScrolling);
  gallery.addEventListener("mouseleave", startScrolling);
});
