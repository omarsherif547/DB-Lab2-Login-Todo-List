
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector(
        'form[data-validate="register"]'
    );

    if (!form) return;

    form.addEventListener("submit", function (event) {

        // Remove previous JavaScript errors
        form.querySelectorAll(".client-error").forEach(
            element => element.remove()
        );

        // Read registration fields
        const name = form.elements.namedItem("name").value.trim();
        const email = form.elements.namedItem("email").value.trim();
        const password = form.elements.namedItem("password").value;
        const confirmPassword =
            form.elements.namedItem("confirm_password").value;

        let errors = [];

        // Validate required fields
        if (!name) {
            errors.push("Name is required");
        }

        if (!email) {
            errors.push("Email is required");
        }

        if (!password) {
            errors.push("Password is required");
        }

        if (!confirmPassword) {
            errors.push("Confirm password is required");
        }

        // Check whether passwords match
        if (password && confirmPassword &&
            password !== confirmPassword) {
            errors.push("Passwords do not match");
        }

        // Stop the form if validation fails
        if (errors.length > 0) {

            event.preventDefault();

            const errorBox = document.createElement("div");
            errorBox.className =
                "alert alert-danger client-error";
            errorBox.setAttribute("role", "alert");

            errors.forEach(function (error) {

                const message = document.createElement("p");
                message.className = "mb-1";
                message.textContent = error;

                errorBox.appendChild(message);

            });

            form.prepend(errorBox);
        }
    });
});

/* ==========================================
   LOGIN FORM VALIDATION
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.querySelector(
        'form[data-validate="login"]'
    );

    if (!loginForm) return;

    loginForm.addEventListener("submit", function (event) {

        // Remove previous validation errors
        loginForm.querySelectorAll(".client-error").forEach(
            element => element.remove()
        );

        // Read input values
        const email = loginForm.elements
            .namedItem("email").value.trim();

        const password = loginForm.elements
            .namedItem("password").value;

        let errors = [];

        // Check required fields
        if (!email) {
            errors.push("Email is required");
        }

        if (!password) {
            errors.push("Password is required");
        }

        // Prevent submission if errors exist
        if (errors.length > 0) {

            event.preventDefault();

            const errorBox = document.createElement("div");

            errorBox.className =
                "alert alert-danger client-error";

            errorBox.setAttribute("role", "alert");

            errors.forEach(function (error) {

                const message = document.createElement("p");

                message.className = "mb-1";
                message.textContent = error;

                errorBox.appendChild(message);

            });

            loginForm.prepend(errorBox);
        }

    });

});

/* ==========================================
   ADD AND EDIT TASK VALIDATION
========================================== */

document.addEventListener("DOMContentLoaded", function () {

    const todoForms = document.querySelectorAll(
        'form[data-validate="todo-title"]'
    );

    todoForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            // Remove previous JavaScript error
            const previousError = form.nextElementSibling;

            if (previousError &&
                previousError.classList.contains("client-error")) {
                previousError.remove();
            }

            // Read the task title
            const title = form.elements
                .namedItem("title").value.trim();

            let errors = [];

            // Validate task title
            if (!title) {
                errors.push("Title is required");
            }

            else if (title.length > 200) {
                errors.push("Title is too long");
            }

            // Stop submission if invalid
            if (errors.length > 0) {

                event.preventDefault();

                const errorBox = document.createElement("div");

                errorBox.className =
                    "alert alert-danger client-error mt-2";

                errorBox.setAttribute("role", "alert");

                errors.forEach(function (error) {

                    const message = document.createElement("p");

                    message.className = "mb-1";
                    message.textContent = error;

                    errorBox.appendChild(message);

                });

                form.insertAdjacentElement("afterend", errorBox);
            }

        });

    });

});
