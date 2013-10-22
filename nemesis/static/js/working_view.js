WorkingView = function() {
    return function(jquerynode) {
        var node = jquerynode;

        this.start = function(text) {
            node.text(text);
            node.show();
        };

        this.end = function(text, milliseconds) {
            var milliseconds = milliseconds || 1000;
            node.text(text);
            setTimeout(this.hide, milliseconds);
        };

        this.hide = function() {
            node.hide();
        };
    }
}();
