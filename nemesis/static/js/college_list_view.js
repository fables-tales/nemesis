var CollegeListView = function() {
    return function(jquery_node) {
        var node = jquery_node;
        var colleges = [];
        var that = this;
        var current_username;
        var allow_registration_last;

        this.render_colleges = function(college_list, allow_registration) {
            colleges = college_list;
            allow_registration_last = allow_registration;

            var college_template = TemplateExpander.template("college");
            var user_template    = TemplateExpander.template("user_link");
            var register_template = null;
            if (allow_registration) {
                register_template = TemplateExpander.template("register_link");
            }

            var result = "";
            var media_consent_template = TemplateExpander.template('media_consent');
            for (var i = 0; i < college_list.length; i++) {
                var college = college_list[i];
                $(college.users).each(function(idx, u) {
                    var args = { 'first': u.first_name,
                                  'last': u.last_name };
                    if (u.has_media_consent) {
                        args.not = '';
                        args.icon = 'camera';
                    } else {
                        args.not = 'not ';
                        args.icon = 'none';
                    }
                    u.media = media_consent_template.render_with(args);
                });
                $.each(college.users, function (index, user) {
                    user.class = user.has_withdrawn ? "disabled" : undefined;
                });
                var user_templates = user_template.map_over("user", college.users);
                var register_link = '';
                if (allow_registration && register_template != null) { // will be null if not allowed to register
                    register_link = register_template.render_with({"college":college});
                }
                var final_render = college_template.render_with({"users":user_templates,
                    "register":register_link,
                    "college":college});

                result += final_render;
            }

            node.html(result);

            $('#data-college-list button.refresh').click(that.refresh);
        };
        this.set_active = function(username) {
            this.set_all_inactive();
            var u = $("." + username);
            if (u.length) {
                u.addClass("active");
                current_username = username;
            } else {
                // not a valid username
                clear_view();
            }
        };

        this.set_all_inactive = function() {
            $(".active").removeClass("active");
            current_username = null;
        };

        this.set_register_active = function(college_name) {
            $("#" + college_name + " .register").addClass("active");
            current_username = null;
        };

        this.refresh = function() {
            var count = colleges.length;
            var u = current_username;
            $(colleges).each(function(i, college) {
                college.reload_users(function() {
                    count -= 1;
                    if (count == 0) {
                        that.render_colleges(colleges, allow_registration_last);
                        if (u) {
                            that.set_active(u);
                        }
                    }
                });
            });
        };
    };
}();
