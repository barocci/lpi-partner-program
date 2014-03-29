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
  self.selected_company = ko.observable(-1);
  self.companies = ko.observableArray([]);

  self.init = function(param) {
      self.handle(param.handle);
      if(lpi.is_logged()) {
        lpi.request('account_info', {section: 'partnership'}, function(response) {
          console.log(response.data);
          var type = ['academic', 'services', 'training'];
          for(i = 0; i < type.length; i++) {
            console.log(type[i]);
            for(j = 0; j < response.data[type[i]].length; j++) {
              self.companies.push(response.data[type[i]][j]);
            }
          }
        });
      }
  };

  self.end = function() {
    self.companies([]);
  };

  self.set_company = function(id) {
    console.log('setting company ' + id);
    self.selected_company(id);
    console.log(this);
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

  self.attach = function() {
     var company = $('input[name=company]:checked').val();
     if(company <= 0) {
        // new company
        lpi.redirect('wizard/' + lpi.user_id + '/' + self.handle());
     } else {
        // existing company
        lpi.post('attach_contact', {company: company, product: self.handle()}, 
          function(response) {
            console.log(response.data);
            if(response.error == 0) {
              console.log('dasdsadas');
              lpi.pages.nav.login();
              lpi.redirect('#account');
            } else {
              self.error_message('Registrazione non valida.');     
            }
          });
     }
  };
}