var WizardViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.company_name = ko.observable();
  self.company_sector = ko.observable();
  self.owner_firstname = ko.observable();
  self.owner_lastname = ko.observable();
  self.owner_role = ko.observable();

  self.init = function(params) {
    self.handle = params.handle
    self.userID = params.userID
  };

  self.submit = function() {
    var data = {
      'company_name': self.company_name(),
      'company_sector': self.company_sector(),
      'owner_firstname': self.owner_firstname(),
      'owner_lastname': self.owner_lastname(),
      'owner_role': self.owner_role(),
      'userID': self.userID,
      'handle': self.handle
    }

    lpi.request('register_contact', data, function(response) {
      lpi.redirect('#account');
    });
  };
}