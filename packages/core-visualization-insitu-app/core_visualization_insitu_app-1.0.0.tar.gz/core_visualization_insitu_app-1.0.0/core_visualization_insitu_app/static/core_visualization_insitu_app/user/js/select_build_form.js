
/**
 * on change of dropdown
 * Update selected build
 */
var onBuildChange = function(event){
    showVisuLoadingSpinner();
    build = $("#select-build-dropdown-form :selected").attr("value");
    $.ajax({
        url : select_build_form,
        type : "GET",
        data : {
            build,
        },
        dataType: "json",
        success: function(data){
           if(data !== null) {
              document.getElementById('select_insitu_forms').innerHTML = data.form;
              $("#select-build-dropdown-form").on("change", onBuildChange);
              $("#select-part-dropdown-form").on("change", onPartChange);
              };
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
    $("#select-build-dropdown-form").on("change", onBuildChange);
});