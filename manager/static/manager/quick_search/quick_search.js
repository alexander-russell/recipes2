const params = new URLSearchParams(window.location.search);
const input = document.querySelector('input');
const allItems = document.querySelectorAll('.search-results li');

// Variable and funciton to store and update which result is focused
let focusedIndex = -1;
function updateFocus(newIndex, itemsArray) {
    if (focusedIndex >= 0) itemsArray[focusedIndex].classList.remove('focused');
    focusedIndex = newIndex;
    if (focusedIndex >= 0 && focusedIndex < itemsArray.length) {
        itemsArray[focusedIndex].classList.add('focused');
        itemsArray[focusedIndex].querySelector('a').scrollIntoView({ block: 'nearest' });
    }
}

// On input, populate results by selectively unhiding existing list items, only first 5
input.addEventListener('input', () => {
    // const query = input.value.toLowerCase();
    const queryRegex = new RegExp(input.value.toLowerCase().trim().replace(/\s+/g, '.*'))
    let resultsCount = 0;

    // Reset focus
    focusedIndex = -1
    document.querySelectorAll(".focused").forEach(element => element.classList.remove("focused"))

    allItems.forEach(li => {
        if (queryRegex.test(li.querySelector('a').textContent.toLowerCase()) && resultsCount < 5) {
            li.classList.remove("hidden");
            resultsCount++;
        } else {
            li.classList.add("hidden");
        }
    });

    if (resultsCount == 1) {
        document.querySelector('.search-results li:not(.hidden)').classList.add("focused")
    }
});

// Listen for keydown to control result actions
document.addEventListener('keydown', (e) => {
    const itemsArray = Array.from(document.querySelectorAll('.search-results li:not(.hidden)'));
    if (e.key === 'ArrowDown' && itemsArray.length != 0) {
        // Move focus down for downarrow
        e.preventDefault();
        if (focusedIndex < itemsArray.length - 1) {
            updateFocus(focusedIndex + 1, itemsArray);
        } else {
            updateFocus(0, itemsArray); // loop to first
        }
    } else if (e.key === 'ArrowUp' && itemsArray.length != 0) {
        // Move focus up for uparrow
        console.log("arrowupped");
        e.preventDefault();
        if (focusedIndex > 0) {
            updateFocus(focusedIndex - 1, itemsArray);
        } else {
            updateFocus(itemsArray.length - 1, itemsArray); // loop to last
        }
    } else if (e.key === 'Enter' && itemsArray.length != 0) {
        // Open focused item (or first one if none are focused)
        e.preventDefault();
        item = (focusedIndex >= 0 && focusedIndex < itemsArray.length) ? itemsArray[focusedIndex] : itemsArray[0];
        link = item.querySelector('a').href;
        window.open(link);
    } else if (e.key === 'Escape') {
        console.log('escapin')
        input.value = '';
        input.dispatchEvent(new Event('input'));
    }
});

// 
if (params.get('query')) {
    input.value = params.get('query');
    input.dispatchEvent(new Event('input'));

    // Clear URL params without reloading the page
    const cleanUrl = window.location.origin + window.location.pathname;
    history.replaceState({}, '', cleanUrl);
}

// Focus the input
input.focus();