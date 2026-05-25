document.addEventListener("DOMContentLoaded", () => {

        // SERVICE SELECTION
        const serviceCards =
        document.querySelectorAll(".booking-service-card");

        let selectedService = null;

        serviceCards.forEach(card => {

            card.addEventListener("click", () => {

                serviceCards.forEach(c => {
                    c.classList.remove("selected");
                });

                card.classList.add("selected");

                selectedService =
                card.querySelector("p").innerText;

            });

        });

        // DATE LIMIT
        const dateInput =
        document.getElementById("appt-date");

        const today =
        new Date().toISOString().split("T")[0];

        dateInput.min = today;

        // TIME SLOT GENERATOR
        const timeContainer =
        document.getElementById("timeSlots");

        let selectedTime = null;

        function generateTimeSlots() {

            timeContainer.innerHTML = "";

            let start = 8 * 60;
            let end = 17 * 60;

            for (let i = start; i <= end; i += 5) {

                let hours = Math.floor(i / 60);

                let minutes = i % 60;

                let ampm =
                hours >= 12 ? "PM" : "AM";

                let displayHour =
                hours % 12 || 12;

                let timeStr =
                `${displayHour}:${minutes
                .toString()
                .padStart(2, "0")} ${ampm}`;

                let btn =
                document.createElement("button");

                btn.classList.add("time-slot");

                btn.innerText = timeStr;

                btn.addEventListener("click", () => {

                    document
                    .querySelectorAll(".time-slot")
                    .forEach(b => {
                        b.classList.remove("selected");
                    });

                    btn.classList.add("selected");

                    selectedTime = timeStr;

                });

                timeContainer.appendChild(btn);

            }

        }

        generateTimeSlots();

        // BOOK APPOINTMENT
        document.querySelector(".btn-primary")
        .addEventListener("click", (e) => {

            e.preventDefault();

            const date = dateInput.value;

            if (!selectedService) {

                alert("Please select a service.");
                return;
            }

            if (!date) {

                alert("Please select a date.");
                return;
            }

            if (!selectedTime) {

                alert("Please select a time.");
                return;
            }

            let appointments =
            JSON.parse(
                localStorage.getItem("appointments")
            ) || [];

            appointments.push({

                service: selectedService,
                date: date,
                time: selectedTime,
                status: "Pending"

            });

            localStorage.setItem(
                "appointments",
                JSON.stringify(appointments)
            );

            alert("Appointment booked successfully!");

            window.location.href =
            "dashboard.html";

        });

    });