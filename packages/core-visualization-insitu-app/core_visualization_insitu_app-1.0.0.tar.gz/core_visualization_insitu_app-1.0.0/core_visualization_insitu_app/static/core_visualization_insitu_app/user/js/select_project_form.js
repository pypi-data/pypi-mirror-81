/**
 * on change of dropdown
 * Update selected project
 */
var onProjectChange = function(event){
    showVisuLoadingSpinner();
    project = $("#select-project-dropdown-form :selected").attr("value");
    $.ajax({
       url: select_project_form,
       type: "GET",
       data : {
            project,
        },
       dataType: "json",
       success: function(data) {
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
    $("#select-project-dropdown-form").on("change", onProjectChange);
});


