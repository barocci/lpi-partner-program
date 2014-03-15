var SignupViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'signup';

  self.mail = ko.observable('');
  self.tos_accepted = ko.observable(false);
  self.password = ko.observable('');
  self.confirm_password = ko.observable('');
  self.handle = ko.observable('');

  self.error_message = ko.observable(null);

  self.init = function(param) {
      self.handle(param.handle);
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
  }

  self.register = function() {
     if(self.mail() == '') {
      self.error_message("Il campo email non puo' essere vuoto.")
      console.log("Il campo email non puo' essere vuoto.")
     }else if(self.password() == '') {
      self.error_message("Il campo password non puo' essere vuoto.")
     }else if(!self.tos_accepted()) {
      self.error_message("&Egrave; necessario accettare i Termini di Servizio per procedere.")
     }else if(self.password() == self.confirm_password()) {
       var params = {
          mail: self.mail(),
          password: self.password(),
          product: self.product_handle
       };

       lpi.request('register', params, function(response) {
          if(!response.error) {
            lpi.redirect('wizard/' + response.data.id + '/' + self.handle());
          } else {
            self.error_message(response['data']);
          }
       });

     } else {
       self.error_message('Le password non combaciano.');
     }
  };


  
}