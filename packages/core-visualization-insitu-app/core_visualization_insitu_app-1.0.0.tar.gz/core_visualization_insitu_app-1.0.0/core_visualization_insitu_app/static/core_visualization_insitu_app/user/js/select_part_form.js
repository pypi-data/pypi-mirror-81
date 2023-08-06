
/**
 * on change of dropdown
 * Update selected part
 */
var onPartChange = function(event){
    showVisuLoadingSpinner();
    part = $("#select-part-dropdown-form :selected").attr("value");
    $.ajax({
        url : select_part_form,
        type : "GET",
        data : {
            part,
        },
        dataType: "json",
        success: function(data){
            loadInfo();
            loadFrames();
            display_3d_visualization();
        },
        error: function(data){
            console.log("Error");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to dropdown button
    $("#select-part-dropdown-form").on("change", onPartChange);
});