document.addEventListener("DOMContentLoaded", () => {

    const studentNameElement = document.getElementById("student-name");

    const storedUser = JSON.parse(localStorage.getItem("user"));

    // USER DISPLAY
    if (storedUser && storedUser.email) {
        studentNameElement.textContent = storedUser.email.split("@")[0];
    } else {
        studentNameElement.textContent = "Guest";
    }

    // GET APPOINTMENTS FROM STORAGE
    let appointments = JSON.parse(localStorage.getItem("appointments")) || [];

    const appointmentContainer = document.querySelector(".appointment-cards");

    appointmentContainer.innerHTML = "";

    // IF NO APPOINTMENTS
    if (appointments.length === 0) {
        const emptyCard = document.createElement("div");
        emptyCard.classList.add("appt-card");
        emptyCard.innerHTML = "<p>No upcoming appointments.</p>";
        appointmentContainer.appendChild(emptyCard);
    } 
    else {
        // RENDER APPOINTMENTS
        appointments.forEach(app => {

            const card = document.createElement("div");
            card.classList.add("appt-card");

            card.innerHTML = `
                <p class="appt-date">${app.date}</p>
                <p class="appt-time">${app.time}</p>
                <p class="appt-service">${app.service}</p>
                <p class="appt-status-label">Status:</p>
                <span class="badge ${app.status.toLowerCase()}">${app.status}</span>
            `;

            appointmentContainer.appendChild(card);
        });
    }

    // SERVICE CLICK ALERTS
    document.querySelectorAll(".service-pill").forEach(service => {
        service.addEventListener("click", () => {
            alert("You selected: " + service.textContent);
        });
    });

    // LOGOUT
    document.querySelector(".nav-logout").addEventListener("click", (e) => {
        e.preventDefault();
        localStorage.clear();
        alert("Logged out!");
        window.location.href = "login.html";
    });

});