var EditView = function() {
    return function(jquerynode, refresh_callback) {
        var jquerynode = jquerynode;
        var that = this;
        var my_user;
        var my_requesting_user;

        this.show = function(target_username, requesting_user) {
            my_user = new User(target_username);
            my_requesting_user = requesting_user;
            this.refresh_view();
        };

        this.refresh_view = function() {
            my_user.fetch(function(user) {
                var template = TemplateExpander.template("user_edit");
                var email_comment = '';
                if (user.new_email !== undefined) {
                    email_comment = " (pending change to " + user.new_email + ")";
                }
                var opts = {"user":user,
                   "email_comment":email_comment,
                     "team_select":that.make_team_select(user)};
                var text = template.render_with(opts);
                jquerynode.html(text);
                jquerynode.show();
                if (user.email === undefined) {
                    $("#data-email").hide();
                } else {
                    $("#data-email").show();
                }
                if (user.new_email === undefined) {
                    $("#edit-cancel-email-change").hide();
                } else {
                    $("#edit-cancel-email-change").show()
                                                  .click(function() {
                        that.cancel_email_change();
                    });
                }
                wv.end("Loaded user successfully!");
                $("#edit-submit").click(function() {
                    that.submit_form();
                });

                refresh_callback();
            });
        };

        this.make_team_select = function(user) {
            return TemplateExpander.make_select('new_team', my_requesting_user.teams, user.teams[0]);
        };

        this.hide = function() {
            jquerynode.hide();
        };

        this.cancel_email_change = function() {
            wv.start("Cancelling outstanding email change");
            $.post("user/" + my_user.username, {'new_email': my_user.email}, function(response) {
                that.refresh_view();
            });
        };

        this.submit_form = function() {
            wv.start("Sending user details");
            $.post("user/" + my_user.username, this.details_on_form(), function(response) {
                that.refresh_view();
            });
        };

        this.details_on_form = function() {
            var details = {};
            if (password_input() != "") {
                details["new_password"] = password_input();
            }

            $("#update-user").find("input[type=text]").each(function(i,element) {
                var $e = $(element);
                details[$e.attr("name")] = $e.val();
            });

            details['new_team'] = $("#update-user select[name=new_team]").val();

            if (details['new_email'] == my_user.email) {
                // If unchanged, we mustn't send the value -- this cancels any outstanding change requests
                delete details['new_email'];
            }

            return details;
        };

        var password_input = function() {
            return $("input[name=new_password]").val();
        };

    };
}();
