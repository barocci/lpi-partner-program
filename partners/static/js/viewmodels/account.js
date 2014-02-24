var AccountViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.require_login = true;

  self.sections = [{name: 'Partnership', slug: 'partnership', products: []},
                   {name: 'Azienda', slug: 'profile', products: []}, 
                   {name: 'Sedi operative', slug: 'location', products: []}, 
                   {name: 'Insegnanti', slug: 'teachers', products: []}, 
                   {name: 'Account', slug: 'account', products: []}, 
                   {name: 'Pagamenti', slug: 'billing', products: []}];


  self.active_section = ko.observable('');

  self.training = ko.observableArray([]);
  self.services = ko.observableArray([]);
  self.academic = ko.observableArray([]);

  self.loading = ko.observable(true);

  self.selected_profile = ko.observable(false);
  self.profile_product = ko.observable(false);

  self.edit = { 
    incharge: ko.observable(false),
    commercial: ko.observable(false),
  }

  self.profiles = {
    'company': {
      'id': ko.observable(''),
      'first_name': ko.observable(''),
      'last_name': ko.observable(''),
      'job_title': ko.observable(''),
      'background': ko.observable(''),
      'street': ko.observable(''),
      'city': ko.observable(''),
      'piva': ko.observable(''),
      'postcode': ko.observable(''),
      'country': ko.observable(''),
      'piva': ko.observable(''),
      'website': ko.observable(''),
      'phone': ko.observable(''),
      'email': ko.observable(''),
      'image_url': ko.observable(''),
      'Role': ko.observable('Company'),
      'type': 'company',
    },

    'incharge': {
      'id': ko.observable(''),
      'first_name': ko.observable(''),
      'last_name': ko.observable(''),
      'job_title': ko.observable(''),
      'background': ko.observable(''),
      'street': ko.observable(''),
      'city': ko.observable(''),
      'postcode': ko.observable(''),
      'country': ko.observable(''),
      'piva': ko.observable(''),
      'website': ko.observable(''),
      'phone': ko.observable(''),
      'email': ko.observable(''),
      'image_url': ko.observable(''),
      'company_id': ko.observable(''),
      'Role': ko.observable('Incharge'),
      'type': 'incharge',
    },

    'commercial': {
      'id': ko.observable(''),
      'first_name': ko.observable(''),
      'last_name': ko.observable(''),
      'job_title': ko.observable(''),
      'background': ko.observable(''),
      'street': ko.observable(''),
      'city': ko.observable(''),
      'postcode': ko.observable(''),
      'country': ko.observable(''),
      'piva': ko.observable(''),
      'website': ko.observable(''),
      'phone': ko.observable(''),
      'email': ko.observable(''),
      'image_url': ko.observable(''),
      'company_id': ko.observable(''),
      'Role': ko.observable('Commercial'),
      'type': 'commercial',
    }
  }

  
  self.init = function() {
    if(!lpi.is_logged()) {
      lpi.redirect('#login');
    }

    self.show_section({slug: 'partnership'});
  }

  self.observe_form = function(data) {
    for(type in self.profiles) {
      if(data[type]) {
        for(i in data[type]) {
          console.log("Setting[" + type + "] " + i + " = " + data[type][i]);
          self.profiles[type][i](data[type][i]?data[type][i]:'');
        }
      }
    }
  }

  self.edit_profile = function(type) {
    var profile = self.profiles[type];
    self.edit[type](true);
  }

  self.abort_edit_profile = function(type) {
    self.edit[type](false);
  }

  self.submit_profile = function(type) {
    var profile = ko.mapping.toJS(self.profiles[type]);
    console.log(profile);
    profile.company = self.profiles.company.first_name()
    profile.company_id = self.profiles.company.id()
    lpi.post('edit_profile', profile, function(response) {
      console.log(response);
      self.edit[type](false);
    });
  }

  self.goto_profile = function(obj) {
    console.log(obj);
    self.selected_profile(obj.id);
    self.profile_product(obj.product.name);
    self.show_section({slug: 'profile'}, obj.id);
  }

  self.show_all_profiles = function() {
    self.selected_profile(false);
    self.profile_product(false);
    self.ready['profile']();
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
        console.log(data);
        self.observe_form(data);
        console.log("----");
        console.log(self.profiles.company.first_name());
      } else {
        lpi.request('account_info', {section: 'partnership'}, function(response) {
          self.ready['partnership'](response);
        });
      }
    }
  }

  self.show_section = function(section, data) {
    console.log('showing ' + section.slug + ' data ' + data);
    self.loading(true);
    lpi.request('account_info', {section: section.slug, data: data}, function(response) {
      if(self.ready[section.slug]) {
        self.ready[section.slug](response.data);
      }
      self.loading(false);
      self.active_section(section.slug);
    });
  }
}