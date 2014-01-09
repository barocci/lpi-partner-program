var LoginViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.mail = ko.observable();
  self.password = ko.observable();
  self.error_message = ko.observable();

  self.login = function() {

  }

  self.recover_password = function() {
    
  }
}