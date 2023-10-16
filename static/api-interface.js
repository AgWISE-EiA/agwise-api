$(document).ready(function () {
    $("#filter-button").on("click", function () {
        const Province = $("#Province").val();
        const District = $("#District").val();
        const AEZ = $("#AEZ").val();
        const Season = $("#Season").val();
        const limit = $("#limit").val();
        const page = $("#page").val();

        // Make a POST request to the API endpoint
        $.ajax({
            url: "/api/v1/fr-potato-api-input",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                Province: Province,
                District: District,
                AEZ: AEZ,
                Season: Season,
                limit: limit,
                page: page,
            }),
            success: function (data) {
                const tableBody = $("#table-body");
                tableBody.empty(); // Clear previous data

                $.each(data, function (index, item) {
                    tableBody.append(
                        `<tr>
                            <td>${item.id}</td>
                            <td>${item.Province}</td>
                            <td>${item.District}</td>
                            <td>${item.AEZ}</td>
                            <td>${item.Season}</td>
                            <td>${item.refYieldClass}</td>
                            <td>${item.lat_lon}</td>
                            <td>${item.Urea}</td>
                            <td>${item.DAP}</td>
                            <td>${item.NPK}</td>
                            <td>${item.expectedYieldReponse}</td>
                            <td>${item.totalFertilizerCost}</td>
                            <td>${item.netRevenue}</td>
                        </tr>`
                    );
                });
            },
            error: function (error) {
                console.error("Error:", error);
            },
        });
    });
});
