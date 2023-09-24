document.addEventListener("DOMContentLoaded", function () {
    const addExecutorBtn = document.getElementById("addExecutorBtn");
    const tableContainer = document.getElementById("tableContainer");

    addExecutorBtn.addEventListener("click", function () {
        tableContainer.style.display = "block";
    });
});