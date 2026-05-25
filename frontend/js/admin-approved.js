let sortDirection = {};
let currentStatusFilter = "All";

// LOAD PROCESSED APPOINTMENTS

const processedAppointments =
    JSON.parse(localStorage.getItem("processedAppointments")) || [];

const tableBody = document.getElementById("approved-body");

// Empty by default
if (processedAppointments.length === 0) {

    tableBody.innerHTML = `
        <tr>
            <td colspan="5" style="text-align:center; padding:20px;">
                No processed appointments yet.
            </td>
        </tr>
    `;

} else {
    renderTable(processedAppointments);
}

// RENDER TABLE

function renderTable(data) {

    tableBody.innerHTML = "";

    data.forEach(app => {

        const row = `
            <tr>
                <td>${app.name}</td>

                <td>${app.service}</td>

                <td style="text-align:center;">
                    ${app.date}
                </td>

                <td style="text-align:center;">
                    ${app.time}
                </td>

                <td style="text-align:center;">
                    <span class="badge ${
                        app.status === "Approved"
                            ? "approved"
                            : "rejected"
                    }">
                        ${app.status}
                    </span>
                </td>
            </tr>
        `;

        tableBody.innerHTML += row;
    });
}

// SORT TABLE

function sortTable(columnIndex) {

    sortDirection[columnIndex] =
        !sortDirection[columnIndex];

    const sorted = [...processedAppointments];

    sorted.sort((a, b) => {

        let valuesA = [
            a.name,
            a.service,
            a.date,
            a.time
        ];

        let valuesB = [
            b.name,
            b.service,
            b.date,
            b.time
        ];

        let valueA = valuesA[columnIndex];
        let valueB = valuesB[columnIndex];

        // Date sorting
        if (columnIndex === 2) {

            return sortDirection[columnIndex]
                ? new Date(valueA) - new Date(valueB)
                : new Date(valueB) - new Date(valueA);
        }

        // Time sorting
        if (columnIndex === 3) {

            return sortDirection[columnIndex]
                ? convertTime(valueA) - convertTime(valueB)
                : convertTime(valueB) - convertTime(valueA);
        }

        // Text sorting
        return sortDirection[columnIndex]
            ? valueA.localeCompare(valueB)
            : valueB.localeCompare(valueA);
    });

    renderTable(sorted);

    updateArrows(columnIndex);
}

// TIME CONVERTER

function convertTime(timeStr) {

    const [time, modifier] = timeStr.split(" ");

    let [hours, minutes] =
        time.split(":").map(Number);

    if (modifier === "PM" && hours !== 12)
        hours += 12;

    if (modifier === "AM" && hours === 12)
        hours = 0;

    return hours * 60 + minutes;
}

// UPDATE SORT ARROWS

function updateArrows(columnIndex) {

    document.querySelectorAll("th span")
        .forEach(span => span.textContent = "⬍");

    document.getElementById(
        `arrow-${columnIndex}`
    ).textContent =
        sortDirection[columnIndex]
            ? "⬆️"
            : "⬇️";
}

// FILTER STATUS

function filterStatus() {

    if (currentStatusFilter === "All") {
        currentStatusFilter = "Approved";
    }
    else if (currentStatusFilter === "Approved") {
        currentStatusFilter = "Rejected";
    }
    else {
        currentStatusFilter = "All";
    }

    let filtered = [...processedAppointments];

    if (currentStatusFilter !== "All") {

        filtered = filtered.filter(app =>
            app.status === currentStatusFilter
        );
    }

    renderTable(filtered);

    document.getElementById("status-arrow")
        .textContent =
            currentStatusFilter === "All"
                ? "▼"
                : currentStatusFilter;
}