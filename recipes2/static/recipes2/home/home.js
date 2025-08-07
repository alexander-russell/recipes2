const input = document.querySelector('input#name');
const items = document.querySelectorAll('.search-results li');

input.addEventListener('input', () => {
    const query = input.value.toLowerCase();
    let resultsCount = 0;

    items.forEach(li => {
        if (li.querySelector('a').textContent.toLowerCase().includes(query) && resultsCount < 5) {
            li.classList.remove("hidden");
            resultsCount++;
        } else {
            li.classList.add("hidden");
        }
    });
});