$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#recommendation_id").val(res.id);
        $("#recommendation_name").val(res.name);
        $("#recommendation_original_product_id").val(res.original_product_id);
        $("#recommendation_product_id").val(res.recommendation_product_id);
        $("#recommendation_product_name").val(res.recommendation_product_name);
        if (res.activated == true) {
            $("#recommendation_activated").val("true");
        } else {
            $("#recommendation_activated").val("false");
        }
        $("#recommendation_reason").val(res.reason);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#recommendation_id").val("");
        $("#recommendation_name").val("");
        $("#recommendation_original_product_id").val("");
        $("#recommendation_product_id").val("");
        $("#recommendation_product_name").val("");       
        $("#recommendation_activated").val("");
        $("#recommendation_reason").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#recommendation_name").val();
        let original_product_id = $("#recommendation_original_product_id").val();
        let recommendation_product_id = $("#recommendation_product_id").val();
        let recommendation_product_name = $("#recommendation_product_name").val();
        let reason = $("#recommendation_reason").val();
        let activated = $("#recommendation_activated").val() == "true";

        let data = {
            "name": name,
            "original_product_id": original_product_id,
            "recommendation_product_id": recommendation_product_id,
            "recommendation_product_name": recommendation_product_name,
            "reason": reason,
            "activated": activated
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        let id = $("#recommendation_id").val();
        let name = $("#recommendation_name").val();
        let original_product_id = $("#recommendation_original_product_id").val();
        let recommendation_product_id = $("#recommendation_product_id").val();
        let recommendation_product_name = $("#recommendation_product_name").val();
        let reason = $("#recommendation_reason").val();
        let activated = $("#recommendation_activated").val() == "true";

        let data = {
            "name": name,
            "original_product_id": original_product_id,
            "recommendation_product_id": recommendation_product_id,
            "recommendation_product_name": recommendation_product_name,
            "reason": reason,
            "activated": activated
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/recommendations/${id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Recommendations
    // ****************************************

    $("#retrieve-btn").click(function () {

        let id = $("#recommendation_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations/${id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        let id = $("#recommendation_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/recommendations/${id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#recommendation_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        let id = $("#recommendation_id").val();
        let name = $("#recommendation_name").val();
        let original_product_id = $("#recommendation_original_product_id").val();
        let recommendation_product_id = $("#recommendation_product_id").val();
        let recommendation_product_name = $("#recommendation_product_name").val();
        let reason = $("#recommendation_reason").val();
        let activated = $("#recommendation_activated").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (reason) {
            if (queryString.length > 0) {
                queryString += '&reason=' + reason
            } else {
                queryString += 'reason=' + reason
            }
        }
        if (activated) {
            if (queryString.length > 0) {
                queryString += '&activated=' + activated
            } else {
                queryString += 'activated=' + activated
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Original Product ID</th>'
            table += '<th class="col-md-2">Recommendation Name</th>'
            table += '<th class="col-md-2">Recommendation ID</th>'
            table += '<th class="col-md-2">Reason</th>'
            table += '<th class="col-md-2">Activated</th>'
            table += '</tr></thead><tbody>'
            let firstRec = "";
            for(let i = 0; i < res.length; i++) {
                let rec = res[i];
                table +=  `<tr id="row_${i}"><td>${rec.id}</td><td>${rec.name}</td><td>${rec.original_product_id}</td><td>${rec.recommendation_product_name}</td><td>${rec.recommendation_product_id}</td><td>${rec.reason}</td><td>${rec.activated}</td></tr>`;
                if (i == 0) {
                    firstRec = rec;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstRec != "") {
                update_form_data(firstRec)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
