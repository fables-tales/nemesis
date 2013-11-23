var User = function() {
    return function(username) {
        this.username = username;
        this.first_name = "";
        this.last_name = "";
        this.email = "";
        var password = "";
        this.colleges = [];
        var that = this;

        this.login = function(pw, success_callback, error_callback) {
            password = pw;
            set_header();
            $.get("user/" + this.username, function(response) {
                if (typeof(response) === "string") {
                    response = JSON.parse(response);
                }
                that.colleges = $.map(response["colleges"], function(v, i) { return new College(v);});
                that.teams = response.teams;
                success_callback(that);
            }).error(function(response) {
                response = response.responseText;
                if (typeof(response) === "string") {
                    response = JSON.parse(response);
                }
                error_callback(response);
            });
        };

        this.fetch = function(callback) {
            $.get("user/" + this.username, function(response) {
                if (typeof(response) === "string") {
                    response = JSON.parse(response);
                }

                that.colleges = response.colleges;
                that.teams = response.teams;
                clone_simple_properties(response, that);

                callback(that);
            });
        };

        var clone_simple_properties = function(from, to) {
            to.first_name   = from.first_name;
            to.last_name    = from.last_name;
            to.email        = from.email;
            to.new_email    = from.new_email;
            to.is_blueshirt = from.is_blueshirt;
            to.is_student   = from.is_student;
            to.is_team_leader = from.is_team_leader;
            to.has_media_consent = from.has_media_consent;
        };

        var set_header = function() {
            var tok = that.username + ':' + password;
            var hash = Base64.encode(tok);
            $.ajaxSetup({
                headers: {
                    'Authorization': "Basic " + hash
                }
            });
        };

    };
}();
