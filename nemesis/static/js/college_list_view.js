var CollegeListView = function() {
    return function(jquery_node) {
        var node = jquery_node;

        this.render_colleges = function(college_list) {
            var college_template = TemplateExpander.template("college");
            var user_template    = TemplateExpander.template("user_link");
            var register_template = TemplateExpander.template("register_link");

            result = "";
            for (var i = 0; i < college_list.length; i++) {
                var college = college_list[i];
                var user_templates = user_template.map_over("user", college.users);
                var final_render = college_template.render_with({"users":user_templates,
                    "register":register_template.render_with({"college":college}),
                    "college":college});

                result += final_render;
            }

            node.html(result);
        };
        this.set_active = function(username) {
            this.set_all_inactive();
            $("." + username).addClass("active");
        };

        this.set_all_inactive = function() {
            $(".active").removeClass("active");
        };

        this.set_register_active = function(college_name) {
            $("#" + college_name + " .register").addClass("active");
        };
    };
}();
