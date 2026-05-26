document.addEventListener("DOMContentLoaded", () => {

        const signupBtn = document.querySelector(".btn-login");
        const inputs = document.querySelectorAll(".input-box input");

        const emailInput = inputs[0];
        const passwordInput = inputs[1];

        if (signupBtn) {
            signupBtn.addEventListener("click", function (e) {

                e.preventDefault(); 

                const email = emailInput.value.trim();
                const password = passwordInput.value.trim();

                // Check empty fields
                if (!email || !password) {
                    alert("Please fill in all fields.");
                    return;
                }

                // Basic email validation
                if (!email.includes("@")) {
                    alert("Please enter a valid email.");
                    return;
                }

                // Create user object
                const user = {
                    email: email,
                    password: password
                };

                // Save to localStorage
                localStorage.setItem("user", JSON.stringify(user));

                alert("Account created successfully!");

                // Redirect to login page
                window.location.href = "login.html";
            });
        }

    });