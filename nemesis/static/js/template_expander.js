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
    },
    "make_checkboxes" : function(name, options, selected) {
        build = "<ul>";

        if (!(selected instanceof Array)) {
            selected = [selected];
        }

        for (var i = 0 ; i < options.length; i++) {
            build += "<li><label>";
            var opt = options[i];
            var selectAttr = $.inArray(opt, selected) >= 0 ? "' checked='checked" : '';
            build += "<input type='checkbox' name='" + name + selectAttr + "' value='" + opt + "'>";
            build += opt;
            build += "</label></li>";
        }

        build += "</ul>";
        return build;
    }
};

var Template = function() {
    return function(template_text) {
        var template_text = template_text;

        this.render_with = function(hash) {
            var build = "";
            for (var i = 0; i < template_text.length; i++) {
                if (template_text.charAt(i) == "{") {
                    var end_of_section = template_text.indexOf("}", i);
                    var key = template_text.substring(i+1, end_of_section);
                    var split = key.split(".");
                    if (split.length == 1) {
                        var majorkey = split[0];
                        build += hash[majorkey];
                    } else {
                        var majorkey = split[0];
                        var minorkey = split[1];
                        build += hash[majorkey][minorkey];
                    }
                    i = end_of_section;
                } else {
                    build += template_text.charAt(i);
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

// node require() based exports.
if (typeof(exports) != 'undefined') {
	exports.Template = Template;
	exports.TemplateExpander = TemplateExpander;
}
