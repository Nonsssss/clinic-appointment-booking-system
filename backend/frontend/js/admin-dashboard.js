// ADMIN PAGE PROTECTION
    const role = localStorage.getItem("userRole");

    if (role !== "admin") {

        alert("Access denied.");

        window.location.href = "login.html";
    }

    // LOGOUT
    const logoutBtn =
        document.querySelector(".nav-logout");

    if (logoutBtn) {

        logoutBtn.addEventListener(
            "click",
            function () {

                localStorage.removeItem(
                    "userRole"
                );
            }
        );
    }

    // SORTING SYSTEM
    let sortDirection = {};

    const headers =
        document.querySelectorAll(
            ".appointments-table th"
        );

    headers.forEach((header, index) => {

        if (index >= 4) return;

        header.style.cursor = "pointer";

        const arrow =
            document.createElement("span");

        arrow.id = `arrow-${index}`;

        arrow.textContent = " ⬍";

        header.appendChild(arrow);

        header.addEventListener(
            "click",
            function () {

                sortTable(index);
            }
        );
    });

    function sortTable(columnIndex) {

        const table =
            document.querySelector(
                ".appointments-table tbody"
            );

        const rows =
            Array.from(
                table.querySelectorAll("tr")
            );

        sortDirection[columnIndex] =
            !sortDirection[columnIndex];

        const sortedRows =
            rows.sort((a, b) => {

                let aText =
                    a.children[columnIndex]
                    .innerText
                    .trim();

                let bText =
                    b.children[columnIndex]
                    .innerText
                    .trim();

                // DATE SORT
                if (columnIndex === 2) {

                    return sortDirection[columnIndex]
                        ? new Date(aText)
                          - new Date(bText)
                        : new Date(bText)
                          - new Date(aText);
                }

                // TIME SORT
                if (columnIndex === 3) {

                    return sortDirection[columnIndex]
                        ? convertTime(aText)
                          - convertTime(bText)
                        : convertTime(bText)
                          - convertTime(aText);
                }

                // TEXT SORT
                return sortDirection[columnIndex]
                    ? aText.localeCompare(bText)
                    : bText.localeCompare(aText);
            });

        table.innerHTML = "";

        sortedRows.forEach(row => {

            table.appendChild(row);
        });

        updateArrows(columnIndex);

        attachButtonEvents();
    }

    // TIME CONVERTER
    function convertTime(timeStr) {

        const [time, modifier] =
            timeStr.split(" ");

        let [hours, minutes] =
            time.split(":").map(Number);

        if (
            modifier === "PM"
            && hours !== 12
        ) {
            hours += 12;
        }

        if (
            modifier === "AM"
            && hours === 12
        ) {
            hours = 0;
        }

        return hours * 60 + minutes;
    }

    // UPDATE SORT ARROWS
    function updateArrows(columnIndex) {

        document.querySelectorAll("th span")
            .forEach(span => {

                span.textContent = " ⬍";
            });

        document.getElementById(
            `arrow-${columnIndex}`
        ).textContent =
            sortDirection[columnIndex]
                ? " ⬆️"
                : " ⬇️";
    }

    // APPROVE / REJECT SYSTEM
    const processedAppointments =
        JSON.parse(
            localStorage.getItem(
                "processedAppointments"
            )
        ) || [];

    const tableBody =
        document.getElementById(
            "requests-body"
        );

    attachButtonEvents();

    // BUTTON EVENTS
    function attachButtonEvents() {

        const approveButtons =
            document.querySelectorAll(
                ".btn-approve"
            );

        const rejectButtons =
            document.querySelectorAll(
                ".btn-reject"
            );

        approveButtons.forEach(button => {

            button.onclick = function () {

                processAppointment(
                    this,
                    "Approved"
                );
            };
        });

        rejectButtons.forEach(button => {

            button.onclick = function () {

                processAppointment(
                    this,
                    "Rejected"
                );
            };
        });
    }

    // PROCESS APPOINTMENT
    function processAppointment(
        button,
        status
    ) {

        const row =
            button.closest("tr");

        const appointment = {

            name:
                row.children[0]
                .innerText
                .trim(),

            service:
                row.children[1]
                .innerText
                .trim(),

            date:
                row.children[2]
                .innerText
                .trim(),

            time:
                row.children[3]
                .innerText
                .trim(),

            status: status
        };

        // Save processed appointment
        processedAppointments.push(
            appointment
        );

        localStorage.setItem(
            "processedAppointments",
            JSON.stringify(
                processedAppointments
            )
        );

        // Remove pending row
        row.remove();

        checkIfEmpty();
    }

    // EMPTY TABLE CHECK
    function checkIfEmpty() {

        const rows =
            tableBody.querySelectorAll("tr");

        if (rows.length === 0) {

            tableBody.innerHTML = `
                <tr>
                    <td colspan="6"
                        style="
                            text-align:center;
                            padding:20px;
                        ">
                        No pending appointment requests.
                    </td>
                </tr>
            `;
        }
    }

    // Initial check
    checkIfEmpty();