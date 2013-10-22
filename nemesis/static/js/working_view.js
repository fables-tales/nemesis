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
            setTimeout(hide_if(text), milliseconds);
        };

        this.hide = function() {
            node.hide();
        };

        var hide_if = function(text) {
            return function() {
                if (node.text() == text) {
                    node.hide();
                }
            };
        };
    }
}();
