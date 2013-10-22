var ActivateView = function() {
    return function(jquerynode, user) {
        var jquerynode = jquerynode;
        var that = this;
        var my_user = user;

        this.show = function(user) {
            var template = TemplateExpander.template("set-password");
            var opts = { "first_name": user.first_name };
            var text = template.render_with(opts);
            jquerynode.html(text);
            jquerynode.show();
            $("#set-password-submit").click(function() {
                that.submit_form(user.username);
            });
            $("input[name=new_password]").focus();
        };

        this.submit_form = function(username) {
            //wv.start("Sending user details");
            var details = this.details_on_form();
            if (!details) {
                return;
            }
            $.post("user/" + my_user.username, details, function(response) {
                that.show_completion();
            });
        };

        this.details_on_form = function() {
            var password_in = $("input[name=new_password]").val();
            var confirm_password = $("input[name=confirm_password]").val();

            if (password_in != confirm_password) {
                error("Passwords don't match.");
                return false;
            }

            if (password_in.length < 6) {
                error("Password too short.");
                return false;
            }

            return { 'new_password': password_in };
        };

        this.show_completion = function() {
            var template = TemplateExpander.template("account-details");
            var text = template.render_with(my_user);
            jquerynode.html(text);
            jquerynode.show();
        }

        var error = function(text) {
            // TODO
            alert(text);
        }
    };
}();
