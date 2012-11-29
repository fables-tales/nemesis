if (JSON === "undefined") {
    JSON = {"parse": function (x) { return eval("(" + x + ")");}}
}

var token = "";
var current_email = "";
var current_userid = "";


var working_timer = null;
var working_count = 0;

var teams = null;

if (window.location.hash !== "") {
    window.location.hash = "";
}

var hash = window.location.hash;

function showWorking() {
    var text = "Working ";
    var i;

    $("#working-alert").show();
    for (i = 0; i < working_count % 4; i++) {
        text += ".";
    }

    $("#working-alert").text(text);
    working_count += 1;
}

function hideWorking() {
    $("#working-alert").fadeOut();
}


function showSpinner() {
    working_timer = setInterval(showWorking, 500);
}

function hideSpinner() {
    working_count = 0;
    clearInterval(working_timer);
    hideWorking();

}

function loadCollegeDialogue() {
    showSpinner();
    $.get("college", {"token": token}, function (resp) {
        var obj = JSON.parse(resp);
        var i;

        if (teams === null) {
            teams = obj.teams;
            addRegistrationField();
        }
        $("#college-name").text(obj.college_name);
        build = [];
        remaining = obj.userids.length;
        for (i = 0; i < obj.userids.length; i++) {
            var userid = obj.userids[i];
            buildUserDetails(userid, obj);
        }

    });
}

function back() {
    $("#user").hide();
    $("#register-users").hide();
    window.location.hash = "#college";

    loadCollegeDialogue();
    current_userid = "";
}

function handleHash(hash) {
    if (hash === "") {
        back();
    }

    if (hash === "college") {
        back();
    }
    if (hash.indexOf("show-") !== -1) {
        var user = hash.slice(6, hash.length);
        showEdit(user);
    }

    if (hash.indexOf("register-users") !== -1) {
        $("#college").hide();
        $("#register-users").show();
    }
}

setInterval(function () {
    if (window.location.hash !== hash) {
        hash = window.location.hash;
        handleHash(hash);
    }
}, 100);

function populateUser(dict, userid) {
    $("#user-name").text(dict.full_name);
    $("#user-email").attr("value", dict.email);
    current_userid = userid;
    current_email = dict.email;
}

function addRegistrationField() {
    var i;
    build = "<tr class='register-row'>";
    build += "<td><input name='first-name' type='text'></input></td>";
    build += "<td><input name='last-name' type='text'></input></td>";
    build += "<td><input name='email' type='text'></input></td>";

    //build the select dropwodwn for teams
    build += "<td><select name='sel'>";
    for (i = 0; i < teams.length; i++) {
        var team = teams[i];
        build +=      "<option value='" + team + "'>" + team + "</option>";
    }
    build += "</select></td>";
    build += "</tr>";

    //add the input to the table
    $("#register-inputs").append(build);
}

function registerDetails(hash) {
    hash.token = token;
    $.post("user/register", hash);
}

function showEdit(userid) {
    showSpinner();
    $.get("user/" + userid, {"token": token}, function (response) {
        $("#college").hide();
        populateUser(JSON.parse(response), userid);
        $("#user").show();
        hideSpinner();
    });
}

function makeUserClickHandler() {
    return function () {
        uid = this.id.split("-1")[1];
        current_userid = uid;
        showEdit(uid);
    };
}


function makeUsersList(obj, list) {
    var i;
    var userid;
    sorted = list.sort(function (a, b) { return a.user_name < b.user_name; });
    html = "<ul>";
    for (i = 0; i < sorted.length; i++) {
        userid = list[i].userid;
        var user_name = list[i].user_name;
        html += "<li><a class='user' id='user-" + userid + "' href='#show-" + userid + "'>" + user_name + "</a></li>";
    }

    html += "</ul>";
    $("#college-users").html(html);

    for (i = 0; i < obj.userids.length; i++) {
        userid = obj.userids[i];
        $("#user-" + userid).onclick = makeUserClickHandler();
    }
}

var remaining = null;
var build = null;

function buildUserDetails(userid, obj) {
    $.get("user/" + userid, {"token": token}, function (resp) {
        var user_name = JSON.parse(resp).full_name;
        build.push({"userid": userid, "user_name": user_name});
        remaining -= 1;
        if (remaining === 0) {
            makeUsersList(obj, build);
            hideSpinner();
            $("#login").hide();
            $("#college").show();
        }
    });
}

function login() {
    var hash = {"username": $("#username").attr("value"),
                "password": $("#password").attr("value")};
    $.post("auth", hash, function (resp) {
        token = JSON.parse(resp).token;
        $("#error").text("Login Successful");
        loadCollegeDialogue();
    }).error(function (fail) {
        obj = JSON.parse(fail.responseText);
        if (obj.error === "invalid credentials") {
            $("#error").text("Username/password incorrect");
        } else if (obj.error === "not a teacher") {
            $("#error").text("You are not a teacher");
        } else if (obj.error === "not in a college") {
            $("#error").text("Your username is not associated with a college! Please contact us");
        } else {
            $("#error").text(obj.error);
        }
    });
}

$(document).ready(function () {
    $("#login").keyup(function (e) {
        var code = e.keyCode;
        if (code === 13) {
            login();
        }
    });

    $("#username").focus(function () {
        text = $("#username").attr("value");
        if (text === "username") {
            $("#username").attr("value", "");
        }
    });

    $("#password").focus(function () {
        text = $("#password").attr("value");
        if (text === "password") {
            $("#password").attr("value", "");
        }
    });

    $(".back").click(function () {
        back();
    });

    $("#set").click(function () {
        opts = {};
        var empty = true;
        if ($("#user-email").attr("value") !== current_email) {
            opts.email = $("#user-email").attr("value");
            empty = false;
        }

        if ($("#user-password").attr("value") !== "") {
            opts.password = $("#user-password").attr("value");
            empty = false;
        }

        if (!empty && current_userid !== "") {
            opts.token = token;
            $.post("user/" + current_userid, opts, function (resp) {
                back();
                $("#msg").text("User details updated successfully!");
            });
        }

        $("#user-password").attr("value", "");

    });

    $("#go").click(login);
    $("#show-register").click(function () {
        $("#college").hide();
        $("#register-users").show();
    });

    $("#add-row").click(addRegistrationField);
    $("#send-register").click(function () {
        var i;
        showSpinner();
        var rows = $(".register-row");
        $("#send-register").attr("disabled", "true");
        var text = $("#send-register").text();
        $("#send-register").text("Sending registrations...");
        for (i = 0; i < rows.length; i++) {
            var row = rows[i];
            var first_name = row.children[0].children[0].value;
            var last_name  = row.children[1].children[0].value;
            var email      = row.children[2].children[0].value;
            var team       = row.children[3].children[0].value;
            var hash = {"first_name": first_name,
                        "last_name" : last_name,
                        "email"     : email,
                        "team"      : team};

            if (first_name !== "" && last_name !== "" && email !== "") {
                registerDetails(hash);
                if (i === rows.length - 1) {
                    $("#msg").text(rows.length + " users registered successfully!");
                }
            }
        }
        $("#send-register").removeAttr("disabled");
        $("#send-register").text(text);
        hideSpinner();
        back();
    });

});
