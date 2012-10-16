$(document).ready(function() {
    $("#username").focus(function() {
        $("#username").attr("value", "");
    });

    $("#password").focus(function() {
        $("#password").attr("value", "");
    });

    console.log("here")
    $("#go").click(function() {
        console.log("cliccked!");
        $.post("/auth", {"username":$("#username").attr("value"),
            "password":$("#password").attr("value")},
            function(resp) {
                console.log(resp);
            });
        });
    });
