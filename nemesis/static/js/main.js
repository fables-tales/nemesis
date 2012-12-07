var TemplateExpander = (function () {
    return function (selector) {
        var getTemplate = function () {
            return $(selector).text();
        };

        this.injectTemplate = function (options) {
            return getTemplate().replace(":{", options);
        };
    };
}());

function loadCollegeDialogue() {
    workingDialogue.showSpinner();
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

var ErrorHandler = (function () {
    return function () {
        this.decodeError = function (code) {
            var result = {
                "invalid credentials": "Username/password incorrect",
                "not a teacher"      : "You are not a team leader",
                "not in a college"   : "Your username is not associated with a college! Please contact us"
            };

            return result[code] || code;
        };
    };
}());

var WorkingDialogue = (function () {
    return function () {
        var working_timer = null;
        var working_count = 0;
        var $dialogue = null;

        this.respondToReady = function () {
            $dialogue = $("#working-alert");
        };

        var showWorking = function () {
            var text = "Working ";
            var i;

            $dialogue.show();
            for (i = 0; i < working_count % 4; i++) {
                text += ".";
            }
            $dialogue.text(text);
            working_count += 1;
        };

        var hideWorking = function () {
            $dialogue.fadeOut();
        };


        this.showSpinner = function () {
            working_timer = setInterval(showWorking, 500);
        };

        this.hideSpinner = function () {
            working_count = 0;
            clearInterval(working_timer);
            hideWorking();
        };
    };
}());

var workingDialogue = new WorkingDialogue();

var token = "";
var current_email = "";
var current_userid = "";

var teams = null;

if (window.location.hash !== "") {
    window.location.hash = "";
}

var Registration = (function () {
    return function () {
        var state = {};
        this.add = function (name, value) {
            state[name] = value;
        };

        this.isValid = function () {
            return state.first_name !== "" &&
                   state.last_name !== "" &&
                   state.email !== "";
        };

        this.getState = function () {
            return state;
        };
    };
}());

var Registrations = (function () {
    return function () {

        var that = this;

        var rows = function () {
            return $(".register-row");
        };

        this.inputs = function (selector) {
            return rows().find(selector);
        };

        var registrationFromRow = function (row) {
            var obj = new Registration();
            that.inputs(":input").each(function (i, e) {
                var $e = $(e);
                obj.add($e.attr("name"), $e.val());
            });

            return obj;
        };

        var registerDetails = function (registration) {
            var hash = registration.getState();
            hash.token = token;
            $.post("user/register", hash);
        };

        this.sendUserRegistrations = function () {
            var i;
            workingDialogue.showSpinner();
            $(this).attr("disabled", "true");
            var text = $("#send-register").text();
            $(this).text("Sending registrations...");
            for (i = 0; i < rows().length; i++) {
                var row = rows()[i];
                var registration = registrationFromRow(row);

                if (registration.isValid()) {
                    registerDetails(registration);
                    if (i === rows().length - 1) {
                        $("#msg").text(rows().length + " users registered successfully!");
                    }
                }
            }

            $(this).removeAttr("disabled");
            $(this).text(text);
            workingDialogue.hideSpinner();
            back();
        };
    };
}());


var hash = window.location.hash;

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
    var build = "";
    for (i = 0; i < teams.length; i++) {
        var team = teams[i];
        build += "<option value='" + team + "'>" + team + "</option>";
    }

    var completeRow = new TemplateExpander("#register-field").injectTemplate(build);

    //add the input to the table
    $("#register-inputs").append(completeRow);
}

function showEdit(userid) {
    workingDialogue.showSpinner();
    $.get("user/" + userid, {"token": token}, function (response) {
        $("#college").hide();
        populateUser(JSON.parse(response), userid);
        $("#user").show();
        workingDialogue.hideSpinner();
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
            workingDialogue.hideSpinner();
            $("#login").hide();
            $("#college").show();
        }
    });
}

function login() {
    var hash = {
        "username": $("#username").attr("value"),
        "password": $("#password").attr("value")
    };

    $.post("auth", hash, function (resp) {
        token = JSON.parse(resp).token;
        $("#error").text("Login Successful");
        loadCollegeDialogue();
    }).error(function (fail) {
        obj = JSON.parse(fail.responseText);
        $("#error").text(new ErrorHandler().decodeError(obj.error));
        $("#password").attr("value", "");
    });
}

$(document).ready(function () {
    workingDialogue.respondToReady();

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

        new Registrations().inputs(":text").each(function (i,e) {
            $(e).attr("value", "");
        });
    });

    $("#add-row").click(addRegistrationField);
    $("#send-register").click(new Registrations().sendUserRegistrations);

});
