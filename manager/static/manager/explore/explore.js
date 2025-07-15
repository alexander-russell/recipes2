document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = this;
	const params = new URLSearchParams(new FormData(form)).toString();
	//const url = form.action + '?' + params;
    const url = form.action; //"{% url 'manager:explore' %}";

	history.pushState(null, '', url);

    fetch(url + '?' + new URLSearchParams(new FormData(form)), {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.results-wrapper').innerHTML = data.html;
    });
});