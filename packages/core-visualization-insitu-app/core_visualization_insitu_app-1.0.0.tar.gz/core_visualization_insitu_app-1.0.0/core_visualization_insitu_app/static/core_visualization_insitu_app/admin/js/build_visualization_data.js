/**
* on click 'Build visualization data'
load and create data lines visualization objects
*/

var loadVisualizationData = function(event){
   showVisuLoadingSpinner();
   $.ajax({
    url: build_visualization_data,
    success: function(data) {
        var dataT = data.data_table_csv;
        var table = loadTable(dataT);
        $('#data_table').html(table);
        document.getElementById('data-lines').innerHTML = "Number of parts with images: "+data.data_lines;
        hideVisuLoadingSpinner();
    },
    error: function(data){
        console.log("Error");
        }
  });
 }

function loadTable(dataT){
     var data_table = dataT.split(/\r?\n|\r/);
     var table = '<div id="table-scroll" style="overflow:auto; margin-top:20px;"><table class="table table-bordered table-striped" width="100%" style="display: block;overflow-x: auto;white-space: nowrap;"><thead>';
     for(var count = 0; count<data_table.length; count++){
        var cell_data = data_table[count].split(",");
        table += '<tr>';
        for(var cell_count=0; cell_count<cell_data.length; cell_count++){
            if(count === 0){
                table += '<th>'+cell_data[cell_count]+'</th>';
            }
            else{
                table += '<td>'+cell_data[cell_count]+'</td>';
            }
        }
     }
     table = table.substring(0, table.length - 13); // one cell to remove at the end
     table += '</thead></table></div>';
     return table;
}

var getTable = function(event){
    showVisuLoadingSpinner();
    $.ajax({
    url: get_visualization_data,
    success: function(data) {
        var dataT = data.data_table_csv;
        var table = loadTable(dataT);
        $('#data_table').html(table);
        document.getElementById('data-lines').innerHTML = "Number of parts with images: "+data.data_lines;
        hideVisuLoadingSpinner();
    },
    error: function(data){
        console.log("Error");
        }
  });
 }

var showVisuLoadingSpinner = function() {
    $('#visualization-panel-transparent-bgd').show();
    $('#visualization-panel-loading').show();
}

var hideVisuLoadingSpinner = function() {
    $('#visualization-panel-transparent-bgd').hide()
    $('#visualization-panel-loading').hide()
}


$(function() {
    hideVisuLoadingSpinner();
    getTable();
    $('#build-visualization-data').on("click", loadVisualizationData);
});

