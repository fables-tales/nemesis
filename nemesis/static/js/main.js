var current_user = null;
var lastHash = "";
var ev = null;
var cv = null;
var rv = null;

$(document).ready(function() {
    if (location.hash.length >= 1) {
        location.hash = "";
    }
    var av = new AuthView($("#login-error"));
    cv = new CollegeListView($("#data-college-list"))
    ev = new EditView($("#data-edit-user"));
    rv = new RegisterView($("#data-register-users"));
    $("#login").submit(function() {
        current_user = new User($("#username").val())
        console.log(current_user.username);
        current_user.login($("#password").val(), function(user) {
            console.log(user);
            var waiting_colleges = user.colleges.length;
            for (var i = 0; i < user.colleges.length; i++) {
                var college = user.colleges[i];
                college.fetch(function (college) {
                    waiting_colleges--;
                    if (waiting_colleges == 0) {
                        cv.render_colleges(user.colleges);
                    };
                });
            }
            $("#login").hide();
        },
        function(response) {
            av.display_auth_error(response["authentication_errors"]);
        });
        return false;
    });

    hashChangeEventListener = setInterval("hashChangeEventHandler()", 50);
});

function hashChangeEventHandler() {
    var newHash = location.hash.split('#')[1];

    if(newHash != lastHash) {
        lastHash = newHash;
        handle_hash();
    }
}

function handle_hash() {
    console.log("hash changed");
    ev.hide();
    rv.hide();
    cv.set_all_inactive();
    if (location.hash.substring(1,5) == "edit") {
        var username = location.hash.substring(6,location.hash.length);
        rv.hide();
        ev.show(username);
        cv.set_active(username);
    } else if (location.hash.substring(1,4) == "reg") {
        var college_name = location.hash.substring(5,location.hash.length);
        rv.show(college_name);
        cv.set_register_active(college_name);
    }
}
