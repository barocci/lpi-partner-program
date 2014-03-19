var WizardViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'wizard';

  self.handle = ko.observable('');
  self.userID = ko.observable('');
  self.company_name = ko.observable();
  self.company_sector = ko.observable();
  self.owner_firstname = ko.observable();
  self.owner_lastname = ko.observable();
  self.owner_role = ko.observable();
  self.owner_phone = ko.observable();
  self.owner_email = ko.observable();
  self.lpic_id = ko.observable();
  self.lpic_verification_code = ko.observable();
  self.confirm_registration = ko.observable(false);

  self.init = function(params) {
    self.handle(params.handle);
    self.userID(params.userID);
  };

  self.check_family = function(family, set) {
    var handles = [self.product_handle];
    var families = family.split(',');

    for(f in families) {
      if(self.handle().indexOf(families[f]) >= 0 ||
          families[f] == '*')
        return true;
    }

    return false;
  };

  self.submit = function() {
    var data = {
      'company_name': self.company_name(),
      'company_sector': self.company_sector(),
      'owner_firstname': self.owner_firstname(),
      'owner_lastname': self.owner_lastname(),
      'owner_role': self.owner_role(),
      'owner_email': self.owner_email(),
      'owner_phone': self.owner_phone(),
      'lpic_id': self.lpic_id(),
      'lpic_verification_code': self.lpic_verification_code(),
      'userID': self.userID,
      'product': self.handle
    };

    lpi.request('register_contact', data, function(response) {
      if(self.check_family("aap,ct")) {
        lpi.logout(true);
        self.confirm_registration(true);
        $('body,html').animate({scrollTop: 0}, 500);
      } else {
        lpi.pages.nav.login();
        lpi.redirect('#account');
      }
    });
  };
}