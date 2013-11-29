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

            $("#data-register-table input[name=first_name]").first().focus();
        };

        this.make_team_select = function(college) {
            return TemplateExpander.make_select('team', college.teams);
        };

        this.add_row = function(canonical_name) {
            var college = Colleges[canonical_name];
            var text = TemplateExpander.template("register-row").render_with({"team_select":this.make_team_select(college)});
            $("#data-register-table").append(text);
            $("#data-register-table input[name=first_name]").last().focus();
        };

        this.register_users = function() {
            var count = 0;
            var registrations = this.registrations_array();
            var submit_count = registrations.length;
            if (submit_count == 0) {
                // errors in all the lines, bail
                return;
            }
            var request_total = registrations.total;
            wv.start("Registering users: " + count + "/" + submit_count);
            $("#register-submit").attr("disabled", true);
            // for each row, try to submit it.
            $(registrations).each(function(i, row_info) {
                // clear feedback before new request
                row_info.feedback_node.text("");
                that.send_registration_hash(row_info.fields, function() {
                    // success callback -- remove the row, see if all done
                    count += 1;
                    row_info.tr.remove();
                    wv.start("Registering users: " + count + "/" + submit_count);
                    // all submissions done
                    if (count == submit_count) {
                        wv.end("Users registered successfully", 4000);
                        // re-enable submission
                        $("#register-submit").attr("disabled", false);
                        // if all rows were submitted (and all worked)
                        // then hide the registration form
                        if (submit_count == request_total) {
                            location.hash = "";
                        }
                    }
                }, function(response) {
                    // failure callback -- show an error
                    count += 1;
                    var human_error = human_readable_error(response.error);
                    row_info.feedback_node.text(human_error);
                    // re-enable the fields
                    $(row_info.tr).find(':input').each(function(i, e) {
                        e.disabled = false;
                    });
                    // all submissions done
                    if (count == submit_count) {
                        // re-enable submission
                        $("#register-submit").attr("disabled", false);
                    }
                });
            });
        };

        this.send_registration_hash = function(hash, success, failure) {
            hash["college"] = college_name_from_hash();
            $.post("registrations", hash, function(response) {
                success(response);
            }).fail(function(response) {
                response = response.responseText;
                if (typeof(response) === "string") {
                    response = JSON.parse(response);
                }
                failure(response);
            });
        };

        this.registrations_array = function() {
            var rows = $("#data-register-table").find("tr");
            inputs = [];
            //1 because we skip the header row
            inputs.total = rows.length - 1;
            for (var i = 1; i < rows.length; i++) {
                var row = rows[i];
                var row_hash = {};
                var feedback_node = $(row).find('.feedback');
                var invalid = false;
                $(row).find(":input").each (function (i, e) {
                    var $e = $(e);
                    var name = $e.attr("name");
                    var val = $e.val();
                    if ($e.attr('required') && val.length == 0) {
                        var human_error = human_readable_error('no_' + name);
                        feedback_node.html(human_error);
                        invalid = true;
                        return false;
                    }
                    row_hash[name] = val;
                });
                if (invalid) {
                    continue;
                }

                $(row).find(":input").each(function (i, e) {
                    e.disabled = true;
                });
                var row_info = { 'tr': row,
                      'feedback_node': feedback_node,
                             'fields': row_hash };

                inputs.push(row_info);
            }

            return inputs;
        };

        var human_readable_error = function(error_code) {
            var errors = { 'BAD_TEAM': "Invalid team requested",
                        'BAD_COLLEGE': "Invalid college requested",
               'DETAILS_ALREADY_USED': "User details already in use",
            'YOU_CANT_REGISTER_USERS': "You are not allowed to register users",
                    // javascript generated errors
                      'no_first_name': "First name is required",
                       'no_last_name': "Second name is required",
                           'no_email': "Email address is required"
                         };
            if (errors.hasOwnProperty(error_code)) {
                return errors[error_code];
            } else {
                return 'Unknown error!';
            }
        };
    };
}();

