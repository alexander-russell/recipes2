function enforceDatalistMatch(inputId, dataListId) {
    const input = document.getElementById(inputId)
    const dataList = document.getElementById(dataListId)
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
        } else if (matchesPartial.length === 1) {
            input.value = matchesPartial[0].value
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

enforceDatalistMatch('id_ingredient', 'ingredient-list')
enforceDatalistMatch('id_unit', 'unit-list')
enforceDatalistMatch('id_source', 'source-list')