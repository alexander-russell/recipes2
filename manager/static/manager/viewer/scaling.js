function scale() {
    const scalables = document.querySelectorAll(".scalable")
    const yieldQuantityInput = document.querySelector("input.yield-quantity")

    // Update scalable values
    const factor = yieldQuantityInput.value ? yieldQuantityInput.value / yieldQuantityInput.getAttribute("data-original-value") : 1;
    for (const scalable of scalables) {
        scalable.textContent = parseFloat((factor * scalable.getAttribute("data-original-value")).toFixed(2));
    }

    // Modify the URL without reload, or strip it out if yield is 0 or the original value
    if (yieldQuantityInput.value != 0 && yieldQuantityInput.value != yieldQuantityInput.getAttribute("data-original-value")) {
        history.pushState({}, "", window.location.href.split('?')[0] + `?yield=${yieldQuantityInput.value}`);
    } else {
        history.pushState({}, "", window.location.href.split('?')[0]);
    }
}