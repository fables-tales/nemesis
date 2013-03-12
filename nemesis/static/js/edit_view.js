var EditView = function() {
    return function(jquerynode) {
        var jquerynode = jquerynode;

        this.show = function(username) {
            var u = new User(username);
            u.fetch(function(user) {
                var text = TemplateExpander.template("user_edit").render_with({"user":user});
                console.log(text);
                console.log(jquerynode);
                jquerynode.html(text);
                jquerynode.show();
            });
        };

        this.hide = function() {
            jquerynode.hide();
        };
    };
}();
