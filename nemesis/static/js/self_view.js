var SelfView = function() {
    return function(jquerynode) {
        var jquerynode = jquerynode;
        var that = this;
        var my_user;

        this.show = function(username) {
            my_user = new User(username);
            $(document).ajaxSuccess(ajaxFilter);
            // initial rendering, with just the username
            render(my_user);
            // trigger a proper render.
            this.refresh_view();
        };

        this.refresh_view = function() {
            my_user.fetch(render);
        };

        var render = function(user) {
            var template = TemplateExpander.template("welcome_link");
            var html = template.render_with(user);
            jquerynode.html(html);
        };

        // Somewhat hacky method to watch for changes to the current user
        var ajaxFilter = function(e, req, opts) {
            if (opts.type.toUpperCase() == 'POST') {
                var url = opts.url;
                var q_idx = url.indexOf('?');
                if (q_idx >= 0) {
                    url = url.substring(0, q_idx);
                }
                if (url == 'user/' + my_user.username) {
                    that.refresh_view();
                }
            }
        };
    };
}();
