$(document).ready(function () {
    
    $("form#registerID").submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);    

        $.post($(this).attr("action"), formData, function(data) {
            alert(data);
        });
    });

});