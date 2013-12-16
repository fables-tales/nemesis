
var te = require('../../nemesis/static/js/template_expander.js');

describe("The Template class", function() {
	var getTemplate = function (text) {
		var templateExpander = new te.Template(text);
		templateExpander.escape = function(t) { return t; };
		return templateExpander;
	};
	it("should be defined", function() {
		expect(te.Template).toBeDefined();
	});
	it("should be possible to instantiate", function() {
		var expander = getTemplate('');
	});
	it("should be possible to render its content", function() {
		var expander = getTemplate('');
		var out = expander.render();
		expect(out).toBe('');
	});
	it("should expand simple template blocks passed", function() {
		var expander = getTemplate('before {tpl} after');
		var out = expander.render_with({ 'tpl': 'bacon' });
		expect(out).toBe('before bacon after');
	});
	it("should cope with simple template values that are empty strings", function() {
		var expander = getTemplate('before {tpl} after');
		var out = expander.render_with({ 'tpl': '' });
		expect(out).toBe('before  after');
	});
	it("should expand all cases of each simple template block passed", function() {
		var expander = getTemplate('before {tpl} mid {tpl} after');
		var out = expander.render_with({ 'tpl': 'bacon' });
		expect(out).toBe('before bacon mid bacon after');
	});
	it("should cope with simple template blocks next to each other", function() {
		var expander = getTemplate('before {a}{b}{c} after');
		var out = expander.render_with({ 'a': 'A', 'b': 'B', 'c': 'C' });
		expect(out).toBe('before ABC after');
	});
	it("should cope with adjacent keyed template values that are empty strings", function() {
		var expander = getTemplate('before {a}{b}{c} after');
		var out = expander.render_with({ 'a': '', 'b': '', 'c': '' });
		expect(out).toBe('before  after');
	});
	it("should escape bad characters in unlabelled template blocks", function() {
		var expander = getTemplate('before {foo} {html:other} after');
		// fake escaping function to prove it's called.
		expander.escape = function(text) {
			return text.toUpperCase();
		}
		var out = expander.render_with({ 'foo':'bad', 'other':'good' });
		expect(out).toBe('before BAD good after');
	});
	it("should expand keyed template blocks passed", function() {
		var expander = getTemplate('before {tpl.first} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'} });
		expect(out).toBe('before bacon after');
	});
	it("should cope with keyed template values that are empty strings", function() {
		var expander = getTemplate('before {tpl.a} after');
		var out = expander.render_with({ 'tpl': {'a': ''} });
		expect(out).toBe('before  after');
	});
	it("should expand all cases of each keyed template block passed", function() {
		var expander = getTemplate('before {tpl.first} mid {tpl.first} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'} });
		expect(out).toBe('before bacon mid bacon after');
	});
	it("should cope with keyed template blocks next to each other", function() {
		var expander = getTemplate('before {tpl.a}{tpl.b}{tpl.c} after');
		var out = expander.render_with({ 'tpl': { 'a': 'A', 'b': 'B', 'c': 'C' } });
		expect(out).toBe('before ABC after');
	});
	it("should cope with adjacent keyed template values that are empty strings", function() {
		var expander = getTemplate('before {tpl.a}{tpl.b}{tpl.c} after');
		var out = expander.render_with({ 'tpl': { 'a': '', 'b': '', 'c': '' } });
		expect(out).toBe('before  after');
	});
	it("should expand mixtures of template blocks (1)", function() {
		var expander = getTemplate('before {tpl.first} {a} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'}, 'a': 'A' });
		expect(out).toBe('before bacon A after');
	});
	it("should expand mixtures of template blocks (2)", function() {
		var expander = getTemplate('before {a} {tpl.first} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'}, 'a': 'A' });
		expect(out).toBe('before A bacon after');
	});
	it("should ignore any extra parameters", function() {
		var expander = getTemplate('before {tpl} after');
		var out = expander.render_with({ 'tpl': 'jam', 'other': 'nope' });
		expect(out).toBe('before jam after');
	});
	it("should ignore any extra keyed parameters", function() {
		var expander = getTemplate('before {tpl.foo} after');
		var out = expander.render_with({ 'tpl': {'foo':'jam', 'other':'nope'} });
		expect(out).toBe('before jam after');
	});
	it("should escape bad characters in unlabelled keyed templates", function() {
		var expander = getTemplate('before {tpl.foo} {html:tpl.other} after');
		// fake escaping function to prove it's called.
		expander.escape = function(text) {
			return text.toUpperCase();
		}
		var out = expander.render_with({ 'tpl': {'foo':'bad', 'other':'good'} });
		expect(out).toBe('before BAD good after');
	});
});
