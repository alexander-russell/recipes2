// Set popup behaviour of cost exclusions list
const exclusionsBox = document.querySelector(".cost-exclusions");
const costAttribute = document.querySelector("span.cost-wrapper");
costAttribute.addEventListener("mouseover", (event) => {
    exclusionsBox.classList.remove("hidden");
});
costAttribute.addEventListener("mousemove", (event) => {
    exclusionsBox.style.left = `${event.x + 10}px`;
    exclusionsBox.style.top = `${event.y + 10}px`;
});
costAttribute.addEventListener("mouseout", (event) => {
    exclusionsBox.classList.add("hidden");
});