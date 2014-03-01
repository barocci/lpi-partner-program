(function (ko, undefined) {
  ko.BaseViewModel = function () {
    var self = this;

    self.selected = ko.observable("");

    self.template = '';
    self.template_loaded = true;
    self.require_login = false;

    self.init = function(args) {};
    self.end = function(page, args) {};

    self.out_transition = function(callback, timeout) {
      if(!timeout) timeout = 1000;
	  this.selected("");
	  setTimeout(callback, timeout);
	};

    self.in_transition = function() {
	  this.selected("prtn-page-selected");
	};
  }
}(ko));