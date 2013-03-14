WorkingView = function() {
    return function(jquerynode) {
        var node = jquerynode;

        this.start = function(text) {
            node.text(text);
            node.show();
        };

        this.end = function(text) {
            node.text(text);
            setTimeout(this.hide, 1000);
        };

        this.hide = function() {
            node.hide();
        };
    }
}();
