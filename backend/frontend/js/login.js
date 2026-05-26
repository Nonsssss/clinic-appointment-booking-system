document.addEventListener("DOMContentLoaded", () => {

    const loginBtn = document.querySelector(".btn-login");
    const inputs = document.querySelectorAll(".input-box input");

    const emailInput = inputs[0];
    const passwordInput = inputs[1];

    function isValidInstitutionalEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email) && email.endsWith("@rtu.edu.ph");
    }

    if (loginBtn) {
        loginBtn.addEventListener("click", function () {

            const email = emailInput.value.trim();
            const password = passwordInput.value.trim();

            if (!email || !password) {
                alert("Please fill in all fields.");
            }
            else if (!isValidInstitutionalEmail(email)) {
                alert("Warning: Email is not an institutional email (@rtu.edu.ph).");
            }
            else {
                alert("Login successful!");
            }

            window.location.href = "dashboard.html";
        });
    }

    });