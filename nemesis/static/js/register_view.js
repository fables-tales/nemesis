var RegisterView = function() {
    return function(jquerynode) {
        var node = jquerynode;
        var that = this;

        this.hide = function() {
            node.hide();
        };

        this.show = function(canonical_name) {
            var college = Colleges[canonical_name];
            var text = TemplateExpander.template("register").render_with({"college":college, "team_select":this.make_team_select(college)});
            node.html(text);
            this.add_row(canonical_name);
            $("#register-submit").attr("disabled", false);
            $("#register-submit").click(function() {
                that.register_users();
            });
            node.show();
        };

        this.make_team_select = function(college) {
            return TemplateExpander.make_select('team', college.teams);
        };

        this.add_row = function(canonical_name) {
            var college = Colleges[canonical_name];
            var text = TemplateExpander.template("register-row").render_with({"team_select":this.make_team_select(college)});
            $("#data-register-table").append(text);
        };

        this.register_users = function() {
            var count = 0;
            var registrations = this.registrations_array();
            var max_count = registrations.length;
            wv.start("Registering users: " + count + "/" + max_count);
            $("#register-submit").attr("disabled", true);
            $(registrations).each(function(i, registration_hash) {
                that.send_registration_hash(registration_hash, function() {
                    count += 1;
                    wv.start("Registering users: " + count + "/" + max_count);
                    if (count == max_count) {
                        wv.start("Users registered successfully");
                        location.hash = "";
                        setTimeout(function() {
                            wv.hide();
                        }, 4000);
                    }
                });
            });
        };

        this.send_registration_hash = function(hash, callback) {
            hash["college"] = college_name_from_hash();
            var feedback_node = hash['feedback_node'];
            delete hash['feedback_node'];
            $.post("registrations", hash, function(response) {
                callback(response);
            }).fail(function(response) {
                $("#register-submit").attr("disabled", false);
                response = response.responseText;
                if (typeof(response) === "string") {
                    response = JSON.parse(response);
                }
                var human_error = human_readable_error(response.error);
                feedback_node.html(human_error);
            });
        };

        this.registrations_array = function() {
            var rows = $("#data-register-table").find("tr");
            inputs = [];
            //1 because we skip the header row
            for (var i = 1; i < rows.length; i++) {
                var row = rows[i];
                var row_hash = {};
                $(row).find(":input").each (function (i, e) {
                    var $e = $(e);
                    row_hash[$e.attr("name")] = $e.val();
                });
                row_hash['feedback_node'] = $(row).find('.feedback');

                inputs.push(row_hash);
            }

            return inputs;
        };

        var human_readable_error = function(error_code) {
            var errors = { 'BAD_TEAM': "Invalid team requested",
                        'BAD_COLLEGE': "Invalid college requested",
               'DETAILS_ALREADY_USED': "User details already in use",
            'YOU_CANT_REGISTER_USERS': "You are not allowed to register users"
                         };
            if (errors.hasOwnProperty(error_code)) {
                return errors[error_code];
            } else {
                return 'Unknown error!';
            }
        };
    };
}();

