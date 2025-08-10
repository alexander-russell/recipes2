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