var onClickAccessLayer = function(event){
    var frame_id = $(this).attr('id').substring(22) + "-page-number";
    var layer_max = $("#"+ frame_id ).text();
    var layer_number = $(this).closest('.input-box').text();

    var box_id = "access-layer-number-" + $(this).attr('id').substring(22);
    var box_content = $("#" + box_id);
    var layer_number = Number(box_content.val());


    var siblings = $(this).parent().siblings().each(function(){
        var class_list = this.classList;
        if (class_list.length >= 2) {
           var iterator = class_list.values();
           for (var value of iterator){
               if (value == 'tabContentActive') { frame_id = this.id;  }
           }
        }
    });

    if (typeof(layer_number) === 'number' && !(isNaN(layer_number))){
        box_content.val('');
        layer_max = layer_max.split('/')[1];
        layer_max = Number(layer_max);
        if ((layer_number >= 1) && (layer_number <= layer_max)){
            $.ajax({
            url: access_layer_number,
            type: "POST",
            data : {
                frame_id,
                layer_number,
            },
            dataType: "json",
            success: function(data) {
            if(layer_number != null) {
                var i;
                for (i = 0; i < data.total_tabs; i++) {
                    document.getElementById(data.data_name+'-title-tab'+data.tab[i].toString()).innerHTML = data.title[i];
                    document.getElementById(data.data_name+'-img-tab'+data.tab[i].toString()).innerHTML = "<img src=\"" + data.image[i] + "\"/>";
                    document.getElementById(data.data_name+'-page-number').innerHTML = data.layer_number.toString() + "/" + data.total_layers.toString();
                    };
                };
            },
        error: function(data){
            console.log("Error");
            }
            });
        }
        else { box_content.val('');;
               alert("Layer number is incorrect.");
              };
     }
     else { box_content.val('');;
                alert("Layer number is incorrect.");
              };
};


// .ready() called.
$(function() {
    $('.btn-validate').on("click", onClickAccessLayer);

});
