var TemplateExpander = {
    "template" : function(template_name) {
        return new Template($("#" + template_name).html());
    },
    "make_select" : function(name, options, selected) {
        build = "<select name='" + name + "'>";

        for (var i = 0 ; i < options.length; i++) {
            var opt = options[i];
            var selectAttr = selected == opt ? "' selected='selected" : '';
            build += "<option value='" + opt + selectAttr + "'>" + opt + "</option>";
        }

        build += "</select>";
        return build;
    }
};

var Template = function() {
    return function(template_text) {
        var template_text = template_text;

        this.render_with = function(hash) {
            var build = template_text;
            for (var i = 0; i < build.length; i++) {
                if (build.charAt(i) == "{") {
                    var end_of_section = build.indexOf("}", i);
                    var key = build.substring(i+1, end_of_section);
                    var split = key.split(".");
                    if (split.length == 1) {
                        var majorkey = split[0];
                        build = build.substring(0, i) + hash[majorkey] + build.substring(end_of_section+1,build.length);
                    } else {
                        var majorkey = split[0];
                        var minorkey = split[1];
                        build = build.substring(0, i) + hash[majorkey][minorkey] + build.substring(end_of_section+1, build.length);
                    }
                }
            }
            return build;
        };

        this.render = function() {
            return this.render_with({});
        },

        this.map_over = function(key, values) {
            var build = [];
            for (var i = 0; i < values.length; i++) {
                var h = {};
                h[key] = values[i];
                build.push(this.render_with(h));
            }
            return build.join("\n");
        };
    };
}();
