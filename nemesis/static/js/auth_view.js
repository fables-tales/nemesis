var AuthView = function() {
    return function(jquery_node) {
        var node = jquery_node;

        this.display_auth_error = function(auth_errors_list) {
            node.text(human_readable_error(auth_errors_list));
        }

        var human_readable_error = function(auth_errors_list) {
            var reasons = {
                       "WRONG_PASSWORD":"Password incorrect"}

            var result = "";
            for (key in reasons) {
                if (reasons.hasOwnProperty(key) && auth_errors_list.indexOf(key) != -1) {
                    result += reasons[key];
                }
            }

            return result;
        };
    }
}();
