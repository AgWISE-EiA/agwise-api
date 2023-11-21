$(document).ready(function () {

    const dataTable = $("#data-table").DataTable({
        columns: [
            {data: "id"},
            {data: "province"},
            {data: "district"},
            {data: "aez"},
            {data: "season"},
            {data: "coordinates"},
            {data: "urea"},
            {data: "dap"},
            {data: "npk"},
            {data: "currentYield"},
            {data: "expectedYield"},
            {data: "fertilizerCost"},
            {data: "netRevenue"}]
    });

    // Function to retrieve and populate data
    function populateDataTable(filterData) {
        // Make an initial GET request to retrieve data on page load
        $.ajax({
            url: "/api/v1/fr-potato", type: "POST", // You can use GET or POST based on your API
            contentType: "application/json", data: JSON.stringify(filterData), success: function (data) {
                dataTable.rows.add(data).draw();
            }, error: function (xhr, status, error) {
                const {error: errorMessage, status: errorStatus} = $.parseJSON(xhr.responseText);
                $("#errorAlert").html("<strong>Error " + errorStatus + ":</strong> " + errorMessage).show();
                console.error("Error:", xhr);
            },
        });
    }

    // Call the function to retrieve and populate data on page load
    populateDataTable({initial: 0});

    $("#filter-button").on("click", function () {
        const Province = $("#Province").val();
        const District = $("#District").val();
        const AEZ = $("#AEZ").val();
        const Season = $("#Season").val();
        const limit = $("#limit").val();
        const page = $("#page").val();

        const filterData = {
            Province: Province, District: District, AEZ: AEZ, Season: Season, limit: limit, page: page,
        };

        populateDataTable(filterData)
    });
});
