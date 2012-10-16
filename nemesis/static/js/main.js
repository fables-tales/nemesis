var token = "";
var current_email = "";
var current_userid = "";

function show_spinner() {

}

function hide_spinner() {
}


function populate_user(dict, userid) {
    $("#user-name").text(dict["full_name"]);
    $("#user-email").attr("value", dict["email"]);
    current_email = dict["email"];
}

function show_edit(userid) {
    $.get("/user/" + userid, {"token":token}, function(response) {
        $("#college").hide();
        populate_user(JSON.parse(response), userid);
        $("#user").show();
    });
}

function load_college_dialogue() {
    show_spinner();
    $.get("/college", {"token":token}, function(resp) {
        hide_spinner();
        var obj = JSON.parse(resp);
        $("#college-name").text(obj["college_name"]);
        var build = "<ul>"
        for (var i = 0; i < obj["userids"].length; i++) {
            userid = obj["userids"][i];
            build += "<li><a class='user' id='user-" + userid + "' href='#show-" + userid + "'>" + userid + "</a></li>";
        }
        $("#college-users").html(build)

        for (var i = 0; i < obj["userids"].length; i++) {
            var userid = obj["userids"][i];
            $("#user-" + userid).click(function() {
                console.log(this.id);
                uid = this.id.split("-")[1];
                console.log(uid);
                current_userid = uid;
                show_edit(uid);
            });
        }
        $("#login").hide();
        $("#college").show();
    });
}
function back() {
    $("#user").hide();
    load_college_dialogue();
    current_userid = "";
}

$(document).ready(function() {
    $("#username").focus(function() {
        $("#username").attr("value", "");
    });

    $("#password").focus(function() {
        $("#password").attr("value", "");
    });

    $("#back").click(function() {
        back();
    });

    $("#set").click(function() {
        opts = {};
        var empty = true;
        if ($("#user-email").attr("value") != current_email) {
            opts["email"] = $("#user-email").attr("value");
            empty = false;
        }

        if ($("#user-password").attr("value") != "") {
            opts["password"] = $("#user-password").attr("value");
            empty = false;
        }

        if (!empty && current_userid != "") {
            opts["token"] = token;
            $.post("/user/" + current_userid, opts, function(resp) {
                back();
            });
        }

        $("#user-password").attr("value", "");

    });

    console.log("here");
    $("#go").click(function() {
        console.log("cliccked!");
        $.post("/auth", {"username":$("#username").attr("value"),
        "password":$("#password").attr("value")},
            function(resp) {
                token = JSON.parse(resp)["token"]
                $("#error").text("login win");
                load_college_dialogue();
            }).error(
            function(fail) {
                console.log("fail");
                obj = JSON.parse(fail.responseText);
                if (obj["error"] == "invalid credentials") {
                    $("#error").text("Username/password incorrect");
                    console.log("invalid credentials");
                } else if (obj["error"] == "not a teacher") {
                    $("#error").text("You are not a teacher");
                }
            });
    });
});
