var EditView = function() {
    return function(jquerynode, refresh_callback) {
        var jquerynode = jquerynode;
        var that = this;
        var my_user;
        var requesting_user;

        this.show = function(target_username, requesting_user_) {
            my_user = new User(target_username);
            requesting_user = requesting_user_;
            this.refresh_view();
        };

        this.refresh_view = function() {
            my_user.fetch(function(user) {
                var template = TemplateExpander.template("user_edit");
                var opts = {"user":user,
                     "team_select":that.make_team_select(user)};
                var text = template.render_with(opts);
                jquerynode.html(text);
                jquerynode.show();
                if (user.email === undefined) {
                    $("#data-email").hide();
                } else {
                    $("#data-email").show();
                }
                wv.end("Loaded user successfully!");
                $("#edit-submit").click(function() {
                    that.submit_form();
                });

                refresh_callback();
            });
        };

        this.make_team_select = function(user) {
            return make_select('new_team', requesting_user.teams, user.teams[0]);
        };

        this.hide = function() {
            jquerynode.hide();
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

            return details;
        };

        var password_input = function() {
            return $("input[name=new_password]").val();
        };

    };
}();
