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

// Add a confirmation dialog for unsaved changes
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

document.addEventListener("DOMContentLoaded", function () {
    // On page load, restore scroll position
    const scrollY = sessionStorage.getItem("admin-scroll-position");
    if (scrollY) {
        window.scrollTo(0, parseInt(scrollY));
        sessionStorage.removeItem("admin-scroll-position");
    }

    const form = document.querySelector("#recipe_form");

    form.addEventListener("submit", function (e) {
        // Check if the pressed button is "Save and continue editing"
        const activeElement = document.activeElement;
        if (activeElement && activeElement.name === "_continue") {
            sessionStorage.setItem("admin-scroll-position", window.scrollY);
        }
    });
});
