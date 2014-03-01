var JoinusViewModel = function() {
	var self = this;
	ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'joinus';



  self.details = ko.observable("");

  self.show_companies = function() {
    self.details('companies');
  }

  self.show_training = function() {
    self.details('training');
  }
}