var SignupViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'signup';

  self.mail = ko.observable('');
  self.password = ko.observable('');
  self.confirm_password = ko.observable('');
  self.product_handle = '';

  self.error_message = ko.observable(null);

  self.init = function(param) {
      self.product_handle = param.handle;
  };

  self.register = function() {
     if(self.mail() == '') {
      self.error_message("Il campo email non puo' essere vuoto.")
      console.log("Il campo email non puo' essere vuoto.")
     }else if(self.password() == '') {
      self.error_message("Il campo password non puo' essere vuoto.")
     }else if(self.password() == self.confirm_password()) {
       var params = {
          mail: self.mail(),
          password: self.password(),
          product: self.product_handle
       };

       lpi.request('register', params, function(response) {
          if(!response.error) {
            lpi.redirect('wizard/' + response.data.id + '/' + self.product_handle);
          } else {
            self.error_message(response['data']);
          }
       });

     } else {
       self.error_message('Le password non combaciano.');
     }
  };


  
}