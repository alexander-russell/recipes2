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

document.addEventListener("DOMContentLoaded", function () {
    const changeForm = document.querySelector("div.submit-row");
    if (!changeForm) return;

    // Get the object ID from the URL if present
    const match = window.location.pathname.match(/\/(\d+)\/change\/$/);
    if (!match) return; // Don't show button on "Add" form

    const slug = document.getElementById("id_slug").value

    // Create the button
    const viewBtn = document.createElement("a");
    viewBtn.href = `/yum/${slug}/`;
    viewBtn.className = "button";
    viewBtn.style = "line-height: 15px; padding: 10px 15px;";
    viewBtn.textContent = "View";
    viewBtn.target = "_blank";

    // Insert into both top and bottom bars
    document.querySelectorAll("div.submit-row").forEach(row => {
        const clone = viewBtn.cloneNode(true);
        row.insertBefore(clone, row.querySelector("a.deletelink"));
    });
});

// Automatically add recipe ID to related item group links
document.addEventListener("DOMContentLoaded", function () {
    // Extract recipe ID from the admin URL: /admin/<app>/recipe/<id>/change/
    var match = window.location.pathname.match(/\/recipe\/(\d+)\/change\//);
    if (!match) return; // No recipe ID (probably new recipe form)
    var recipeId = match[1];

    // Patch all add-related (+) links pointing to "*group/add/"
    document.querySelectorAll(".add-related").forEach(function (link) {
        if (link.href.match(/group\/add\/\?/)) {
            var sep = link.href.includes("?") ? "&" : "?";
            if (!link.href.includes("recipe=")) {
                link.href += sep + "recipe=" + recipeId;
            }
        }
    });
});