$(document).ready(function () {

    const dataTable = $("#data-table").DataTable({
        columns: [{data: "id"}, {data: "Province"}, {data: "District"}, {data: "AEZ"}, {data: "Season"}, {data: "refYieldClass"}, {data: "lat_lon"}, {data: "Urea"}, {data: "DAP"}, {data: "NPK"}, {data: "expectedYieldReponse"}, {data: "totalFertilizerCost"}, {data: "netRevenue"}]
    });

    // Function to retrieve and populate data
    function retrieveAndPopulateData(filterData) {
        // Make an initial GET request to retrieve data on page load
        $.ajax({
            url: "/api/v1/fr-potato-api-input", type: "POST", // You can use GET or POST based on your API
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
    retrieveAndPopulateData({initial: 0});

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

        retrieveAndPopulateData(filterData)
    });
});
