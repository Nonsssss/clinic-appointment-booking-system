    document.addEventListener("DOMContentLoaded", () => {

        const appointmentContainer =
        document.getElementById("appointmentHistory");

        let appointments =
        JSON.parse(localStorage.getItem("appointments")) || [];

        appointmentContainer.innerHTML = "";

        // NO APPOINTMENTS
        if (appointments.length === 0) {

            appointmentContainer.innerHTML = `
                <tr>
                    <td colspan="4"
                    style="
                    text-align:center;
                    padding: 30px;
                    font-size:18px;
                    ">
                        No appointments yet.
                    </td>
                </tr>
            `;

            return;
        }

        // DISPLAY APPOINTMENTS
        appointments.forEach(appointment => {

            let badgeClass = "";

            // STATUS DESIGN
            if (appointment.status === "Pending") {
                badgeClass = "pending";
            }

            if (appointment.status === "Completed") {
                badgeClass = "done";
            }

            // CREATE TABLE ROW
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${appointment.service}</td>
                <td>${appointment.date}</td>
                <td>${appointment.time}</td>

                <td>
                    <span class="badge ${badgeClass}">
                        ${appointment.status}
                    </span>
                </td>
            `;

            appointmentContainer.appendChild(row);

        });

    });