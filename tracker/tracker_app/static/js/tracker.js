document.addEventListener("DOMContentLoaded", function () {
    const yearSelect = document.getElementById("year-select");
    const monthSelect = document.getElementById("month-select");
    
    function submitForm() {
        const form = yearSelect.closest("form");
        form.submit();
    }

    yearSelect.addEventListener("change", submitForm);
    monthSelect.addEventListener("change", submitForm);
});