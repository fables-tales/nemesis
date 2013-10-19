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

                that.first_name = response.first_name;
                that.last_name = response.last_name;
                that.email = response.email;
                that.new_email = response.new_email;
                that.colleges = response.colleges;
                that.teams = response.teams;
                that.is_blueshirt = response.is_blueshirt;
                that.is_student = response.is_student;
                that.is_team_leader = response.is_team_leader;
                that.has_media_consent = response.has_media_consent;
                callback(that);
            });
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
