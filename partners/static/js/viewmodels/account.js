var AccountViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.sections = [{name: 'Partnership', slug: 'partnership'},
                   {name: 'Profilo', slug: 'profile'}, 
                   {name: 'Account', slug: 'account'}, 
                   {name: 'Pagamenti', slug: 'billing'}, 
                   {name: 'Ordini', slug: 'orders'}, 
                   {name: 'Messaggi', slug: 'messages'}];

  self.active_section = ko.observable('');

  self.training = ko.observableArray([]);
  self.services = ko.observableArray([]);
  self.academic = ko.observableArray([]);

  self.loading = ko.observable(true);

  self.selected_profile = ko.observable(false);
  self.profile_product = ko.observable(false);

  self.init = function() {
    if(!lpi.is_logged()) {
      lpi.redirect('#login');
    }

    self.show_section({slug: 'partnership'});
  }

  self.goto_profile = function(obj) {
    self.selected_profile(obj.company);
    self.profile_product(obj.product.name);
    self.show_section({slug: 'profile'});
  }

  self.show_all_profiles = function() {
    self.selected_profile(false);
    self.profile_product(false);
    self.ready['profile']();
  }

  self.state = function(value) {
    if(value == "True")
      return "Attivo"
    else
      return "Non attivo"
  }

  self.ready = {
    partnership: function(data) {
      console.log(data);

      self.training(data.training);
      self.services(data.services);
      self.academic(data.academic);
    },

    profile: function(data) {
      if(self.selected_profile()) {
        lpi.request('profile',{id: self.selected_profile()}, function(response) {
          console.log(response);
        });
      } else {
        lpi.request('account_info', {section: 'partnership'}, function(response) {
          self.ready['partnership'](response);
        });
      }

    }
  }

  self.show_section = function(section, data) {
    self.loading(true);

    lpi.request('account_info', {section: section.slug}, function(response) {
      if(self.ready[section.slug]) {
        self.ready[section.slug](response.data);
      }
      self.loading(false);
      self.active_section(section.slug);
    });
  }
}