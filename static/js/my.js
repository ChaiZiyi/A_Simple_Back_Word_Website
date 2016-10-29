$("input[name=username]").on("input", $("input[name=password]").on("input", function(evt) {
    if ($(this).val().trim().length) {
        $("#submitbtn").removeAttr("disabled");
    } else {
        $("#submitbtn").prop("disabled", "disabled");
    }
}));

$("input[name=note]").on("input",function(evt) {
    if ($(this).val().trim().length) {
        $("#submitbtn").removeAttr("disabled");
    } else {
        $("#submitbtn").prop("disabled", "disabled");
    }
});
