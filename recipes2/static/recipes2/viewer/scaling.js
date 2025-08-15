function scale() {
    const yieldQuantityInput = document.querySelector("input.yield-quantity")
    const factor = yieldQuantityInput.value ? yieldQuantityInput.value / yieldQuantityInput.getAttribute("data-original-value") : 1;
    
    // Update scalable values
    const scalables = document.querySelectorAll(".scalable")
    for (const scalable of scalables) {
        scalable.textContent = parseFloat((factor * scalable.getAttribute("data-original-value")).toFixed(2));
    }

    // Update scalable-text values
    const words = document.querySelectorAll(".scalable-word");
    for (const word of words) {
        word.textContent = factor * word.getAttribute("data-original-quantity") == 1 ? word.getAttribute("data-singular") : word.getAttribute("data-plural");
    }

    // Modify the URL without reload, or strip it out if yield is 0 or the original value
    if (yieldQuantityInput.value != 0 && yieldQuantityInput.value != yieldQuantityInput.getAttribute("data-original-value")) {
        history.pushState({}, "", window.location.href.split('?')[0] + `?yield=${yieldQuantityInput.value}`);
    } else {
        history.pushState({}, "", window.location.href.split('?')[0]);
    }
}