var _CollectiveCitationstylesInfo = function () {

    // There can only be one
    if ( arguments.callee._singletonInstance )
        return arguments.callee._singletonInstance;
    arguments.callee._singletonInstance = this;
    var csl_map = {};
    var locale_map = {};
    var available_csl = [];
    var available_locale = [];

    this.abbreviations = {"default": {}};
    this.default_csl = '';
    this.default_locale = '';

    this.add_csl = function(name, value) {
        csl_map[name] = value;
        available_csl.push(name);
    }

    this.available_styles = function() {
        return available_csl.sort();
    }

    this.add_locale = function(name, value) {
        locale_map[name] = value;
        available_locale.push(name);
    }


    this.available_locales = function() {
        return available_locale.sort();
    }

    this.retrieveLocale = function(name) {
        return locale_map[name];
    }

    this.retrieveItem = function() {
        // Not Implemented
        return '';
    }

    this.retrieveCSL = function(name) {
        if (!name) {  name = this.default_csl; }
        return csl_map[name];
    }

    this.getAbbreviations = function () {
        // Return empty abbreviation info. This should be retrieved
        // from the control panel via AJAX
        return this.abbreviations;
    }
}

// This is the object passed as the first argument (`sys`) to CSL.Engine
var collective_csl_info = new _CollectiveCitationstylesInfo();

