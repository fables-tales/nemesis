
var te = require('../../nemesis/static/js/template_expander.js');

describe("The Template class", function() {
	it("should be defined", function() {
		expect(te.Template).toBeDefined();
	});
	it("should be possible to instantiate", function() {
		var expander = new te.Template('');
	});
	it("should be possible to render its content", function() {
		var expander = new te.Template('');
		var out = expander.render();
		expect(out).toBe('');
	});
	it("should expand simple template blocks passed", function() {
		var expander = new te.Template('before {tpl} after');
		var out = expander.render_with({ 'tpl': 'bacon' });
		expect(out).toBe('before bacon after');
	});
	it("should cope with simple template values that are empty strings", function() {
		var expander = new te.Template('before {tpl} after');
		var out = expander.render_with({ 'tpl': '' });
		expect(out).toBe('before  after');
	});
	it("should expand all cases of each simple template block passed", function() {
		var expander = new te.Template('before {tpl} mid {tpl} after');
		var out = expander.render_with({ 'tpl': 'bacon' });
		expect(out).toBe('before bacon mid bacon after');
	});
	it("should cope with simple template blocks next to each other", function() {
		var expander = new te.Template('before {a}{b}{c} after');
		var out = expander.render_with({ 'a': 'A', 'b': 'B', 'c': 'C' });
		expect(out).toBe('before ABC after');
	});
	it("should cope with adjacent keyed template values that are empty strings", function() {
		var expander = new te.Template('before {a}{b}{c} after');
		var out = expander.render_with({ 'a': '', 'b': '', 'c': '' });
		expect(out).toBe('before  after');
	});
	it("should expand keyed template blocks passed", function() {
		var expander = new te.Template('before {tpl.first} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'} });
		expect(out).toBe('before bacon after');
	});
	it("should cope with keyed template values that are empty strings", function() {
		var expander = new te.Template('before {tpl.a} after');
		var out = expander.render_with({ 'tpl': {'a': ''} });
		expect(out).toBe('before  after');
	});
	it("should expand all cases of each keyed template block passed", function() {
		var expander = new te.Template('before {tpl.first} mid {tpl.first} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'} });
		expect(out).toBe('before bacon mid bacon after');
	});
	it("should cope with keyed template blocks next to each other", function() {
		var expander = new te.Template('before {tpl.a}{tpl.b}{tpl.c} after');
		var out = expander.render_with({ 'tpl': { 'a': 'A', 'b': 'B', 'c': 'C' } });
		expect(out).toBe('before ABC after');
	});
	it("should cope with adjacent keyed template values that are empty strings", function() {
		var expander = new te.Template('before {tpl.a}{tpl.b}{tpl.c} after');
		var out = expander.render_with({ 'tpl': { 'a': '', 'b': '', 'c': '' } });
		expect(out).toBe('before  after');
	});
	it("should expand mixtures of template blocks (1)", function() {
		var expander = new te.Template('before {tpl.first} {a} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'}, 'a': 'A' });
		expect(out).toBe('before bacon A after');
	});
	it("should expand mixtures of template blocks (2)", function() {
		var expander = new te.Template('before {a} {tpl.first} after');
		var out = expander.render_with({ 'tpl': {'first': 'bacon'}, 'a': 'A' });
		expect(out).toBe('before A bacon after');
	});
	it("should ignore any extra parameters", function() {
		var expander = new te.Template('before {tpl} after');
		var out = expander.render_with({ 'tpl': 'jam', 'other': 'nope' });
		expect(out).toBe('before jam after');
	});
	it("should ignore any extra keyed parameters", function() {
		var expander = new te.Template('before {tpl.foo} after');
		var out = expander.render_with({ 'tpl': {'foo':'jam', 'other':'nope'} });
		expect(out).toBe('before jam after');
	});
});
