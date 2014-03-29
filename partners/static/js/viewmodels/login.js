var LoginViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'login';
  
  self.mail = ko.observable();
  self.password = ko.observable();
  self.error_message = ko.observable();

  self.handle = ko.observable('');

  self.init = function(arg) {
    if(lpi.is_logged()) {
      lpi.redirect('#account');
    }

    if(arg) {
      self.handle(arg.handle);
    }
  }

  self.end = function() {
    self.password('')
    self.error_message('');
  }

  self.login = function() {
    var data = { username: self.mail(), password: self.password()};

    lpi.request('login', data, function(response) {
      lpi.login(response);
      if(response.error != 1) {
        lpi.authenticate();
        if(self.handle() != '') {
          lpi.redirect('#signup/' + self.handle());
        } else {
          lpi.redirect('#account');
        }
      } else {
        self.error_message('Username o password errati.');
      }
    });
  }

  self.recover_password = function() {
  }
}