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
            var max_count = this.registrations_array().length;
            wv.start("Registering users: " + count + "/" + max_count);
            $(this.registrations_array()).each(function(i, registration_hash) {
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
            $.post("registrations", hash, function(response) {
                callback(response);
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

                inputs.push(row_hash);
            }

            return inputs;
        };

    };
}();

