var SignupViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'signup';

  self.company_name = ko.observable('');
  self.last_name = ko.observable('');
  self.mail = ko.observable('');
  self.tos_accepted = ko.observable(false);
  self.privacy_accepted = ko.observable(false);
  self.password = ko.observable('');
  self.confirm_password = ko.observable('');
  self.handle = ko.observable('');

  self.error_message = ko.observable(null);
  self.selected_company = ko.observable(-1);
  self.companies = ko.observableArray([]);

  self.init = function(param) {
    self.handle(param.handle);
    if(lpi.is_logged()) {
      lpi.request('account_info', {section: 'init'}, function(response) {
        var type = ['academic', 'services', 'training'];
        for(i = 0; i < type.length; i++) {
          for(j = 0; j < response.data[type[i]].length; j++) {
            self.companies.push(response.data[type[i]][j]);
          }
        }

        self.set_company(-1);

      });
    }
  };

  self.end = function() {
    self.companies([]);
  };

  self.set_company = function(id) {
    console.log('setting company ' + id);
    self.selected_company(id);
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
    }else if(self.company_name() == '') {
      self.error_message("Il campo nome non puo' essere vuoto.")
    }else if(!self.tos_accepted()) {
      self.error_message("&Egrave; necessario accettare i Termini di Servizio per procedere.")
    }else if(!self.privacy_accepted()) {
      self.error_message("&Egrave; necessario accettare l'informativa sulla Privacy.")
    }else if(self.password() == self.confirm_password()) {
      var params = {
        company_name: self.company_name(),
        last_name: self.last_name(),
        mail: self.mail(),
        password: self.password(),
        product: self.handle()
      };

      lpi.request('register', params, function(response) {
        if(!response.error) {
          lpi.login(response.data);
          lpi.redirect('account/partnership');
        } else {
          self.error_message(response['data']);
        }
      });
    } else {
      self.error_message('Le password non combaciano.');
    }
  };

  self.attach = function() {
     var company = self.selected_company();
     if(company <= 0) {
        // new company
        self.register();
     } else {
        // existing company
        lpi.post('attach_contact', {company: company, product: self.handle()}, 
          function(response) {
            console.log(response.data);
            if(response.error == 0) {
              console.log('dasdsadas');
              lpi.login(response.data);
              lpi.redirect('account/partnership');
            } else {
              self.error_message('Registrazione non valida.');     
            }
          });
     }
  };
}
