var EditView = function() {
    return function(jquerynode, refresh_callback) {
        var jquerynode = jquerynode;
        var that = this;
        var my_user;

        this.show = function(username) {
            my_user = new User(username);
            this.refresh_view();
        };

        this.refresh_view = function() {
            my_user.fetch(function(user) {
                var text = TemplateExpander.template("user_edit").render_with({"user":user});
                console.log(text);
                console.log(jquerynode);
                jquerynode.html(text);
                jquerynode.show();
                wv.end("Loaded user successfully!");
                $("#edit-submit").click(function() {
                    that.submit_form();
                });

                refresh_callback();
            });
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

            return details;
        };

        var password_input = function() {
            return $("input[name=new_password]").val();
        };

    };
}();
