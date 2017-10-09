var deleting = false;
function delete_questions(){
    if(deleting) return;
    deleting = true;

    selected = []
    $(".checkbox-del").each(function(){
        var checkbox = $(this)
        if(checkbox.is(":checked")) selected.push(checkbox.attr("id"));
    })

    data = {
        questionids: selected
    };

    $.ajax({
        url: "/staff/questions/ajax-delete-questions",
        method: "POST",
        data:JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            location.reload();
        }
    });
}

function show_delete(){
    if(!$("#delete_options").hasClass("collapse in")){
        $("#delete_options").collapse("show");
    } else {
        $("#delete_options").collapse("hide");
    }
}

$("#delete_options").on('show.bs.collapse', function(){
    $(".checkbox-del").show();
    $(".table-id").hide();
})

$("#delete_options").on('hide.bs.collapse', function(){
    $(".checkbox-del").hide();
    $(".table-id").show();
})