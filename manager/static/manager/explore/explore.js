document.getElementById('search-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = this;
    const url = form.action.split("?")[0] + '?' + new URLSearchParams(new FormData(form))

    history.pushState(null, '', url);

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => response.json())
        .then(data => {
            document.querySelector('.results-wrapper').innerHTML = data.html;
        });
});