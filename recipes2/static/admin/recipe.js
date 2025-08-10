document.addEventListener("DOMContentLoaded", function () {
    // Select inputs you want to skip in tab order, e.g. readonly fields, certain selects
    const skipSelectors = [
        '.related-widget-wrapper a.related-widget-wrapper-link',
    ];

    skipSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.setAttribute("tabindex", "-1");
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#recipe_form");
    let isDirty = false;

    // Mark form as dirty when any input changes
    form.addEventListener("change", function () {
        isDirty = true;
    });

    // When the form is submitted, reset isDirty flag
    form.addEventListener("submit", function () {
        isDirty = false;
    });

    // Warn on page unload if form is dirty
    window.addEventListener("beforeunload", function (e) {
        if (isDirty) {
            const confirmationMessage = "You have unsaved changes. Are you sure you want to leave?";
            (e || window.event).returnValue = confirmationMessage; // For older browsers
            return confirmationMessage; // For modern browsers
        }
    });
});
