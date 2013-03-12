var RegisterView = function() {
    return function(jquerynode) {
        var node = jquerynode;

        this.hide = function() {
            node.hide();
        };

        this.show = function(canonical_name) {
            var text = TemplateExpander.template("register").render_with({"college":Colleges[canonical_name]});
            node.html(text);
            node.show();
        };
    };
}();

