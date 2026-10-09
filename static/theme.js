
document.addEventListener("DOMContentLoaded", function () {

    // Find the Dark Mode button
    const themeButton = document.getElementById("theme-toggle");

    // Read the previously selected theme
    const savedTheme = localStorage.getItem("theme") || "light";

    // Apply the saved theme
    document.documentElement.setAttribute(
        "data-bs-theme",
        savedTheme
    );

    if (!themeButton) return;

    // Update the button text
    function updateButton() {
        const currentTheme = document.documentElement
            .getAttribute("data-bs-theme");

        themeButton.textContent =
            currentTheme === "dark" ? "Light Mode" : "Dark Mode";
    }

    updateButton();

    // Switch between Dark and Light Mode
    themeButton.addEventListener("click", function () {

        const currentTheme = document.documentElement
            .getAttribute("data-bs-theme");

        const newTheme =
            currentTheme === "dark" ? "light" : "dark";

        // Change Bootstrap theme
        document.documentElement.setAttribute(
            "data-bs-theme",
            newTheme
        );

        // Remember user's preference
        localStorage.setItem("theme", newTheme);

        updateButton();
    });
});
