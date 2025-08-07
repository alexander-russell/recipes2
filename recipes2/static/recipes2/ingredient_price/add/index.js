const form = document.querySelector("form");
const focusable = Array.from(form.querySelectorAll("input:not([type=hidden])"))

function enforceDatalistMatchAndThen(inputId, datalistId, callback = () => { }) {
    const input = document.getElementById(inputId)
    const dataList = document.getElementById(datalistId)
    const options = Array.from(dataList.options)

    // Prevent focus exit (unless blank or only 1 matching option)
    input.addEventListener('blur', () => {
        const value = input.value.trim()

        // Allow leaving if blank
        if (value === '') {
            input.setCustomValidity('')
            return
        }

        // Determine matching options
        const matchesExact = options.filter((o) => o.value.toLowerCase() === value.toLowerCase())
        const matchesPartial = options.filter((o) => o.value.toLowerCase().includes(value.toLowerCase()))

        // If one exact option, use that, otherwise if one partial option, use that, otherwise display error and prevent exit
        if (matchesExact.length === 1) {
            input.value = matchesExact[0].value
            callback(input.value)
        } else if (matchesPartial.length === 1) {
            input.value = matchesPartial[0].value
            callback(input.value)
        } else {
            input.setCustomValidity('Select a valid option')
            input.reportValidity()
            input.focus()
        }
    })

    // Clear error on input
    input.addEventListener('input', () => {
        input.setCustomValidity('')
    })
}

function fetchAndPrefillFromIngredient(name) {
    fetch(`/yum/api/latest-ingredient/?name=${encodeURIComponent(name)}`)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
            if (data) {
                document.getElementById("id_price").value = data.price
                document.getElementById("id_quantity").value = data.quantity
                document.getElementById("id_unit").value = data.unit
                document.getElementById("id_source").value = data.source
            }
        })
        .catch(err => {
            console.warn("Could not fetch latest ingredient price", err)
        })
}

enforceDatalistMatchAndThen('id_ingredient', 'ingredient-list', fetchAndPrefillFromIngredient)
enforceDatalistMatchAndThen('id_unit', 'unit-list')
enforceDatalistMatchAndThen('id_source', 'source-list')

form.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        const index = focusable.indexOf(document.activeElement);
        if (index > -1 && index < focusable.length - 1) {
            event.preventDefault();
            focusable[index + 1].focus();
        }
    }
});

setTimeout(() => {
    const container = document.getElementById('toast-container');
    if (container) {
        container.style.transition = 'opacity 0.5s ease';
        container.style.opacity = '0';
        setTimeout(() => container.remove(), 500); // wait for fade-out before removal
    }
}, 2000);
