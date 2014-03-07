var AccountViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'account';

  self.tags = [ 
                 'PHP', 
                 'Python',
                 'Web Servers',
                 'Sysadmin',
                 'Javascript',
                 'Web'
              ];

  self.require_login = true;

  
  self.sections = [{name: 'Partnership', slug: 'partnership', visible: '*'},
                   {name: 'Azienda', slug: 'profile', visible: 'atp,aap,sp'}, 
                   {name: 'Profilo', slug: 'profile', visible: 'ct'}, 
                   {name: 'Sedi operative', slug: 'locations', visible: 'atp,aap,sp'}, 
                   {name: 'Insegnanti', slug: 'teachers', visible: 'atp,aap'}, 
                   {name: 'Account', slug: 'account', visible: '*'},
                   //{name: 'Pagamenti', slug: 'billing', visible: true}
                   ];


  self.active_section = ko.observable('');

  self.training  = ko.observableArray([]);
  self.services = ko.observableArray([]);
  self.academic = ko.observableArray([]);

  self.active_subscriptions = ko.computed(function() {
    var products = [];
    var subs = self.training();
    subs = subs.concat(self.services());
    subs = subs.concat(self.academic());

    for(i in subs) {
      if(subs[i].product) {
        products.push(subs[i].product.handle);
      }
    }

    return products;
  });

  self.loading = ko.observable(true);

  self.management_url = ko.observable('');

  self.selected_profile = ko.observable(false);
  self.profile_product = ko.observable(false);

  self.edit = { 
    incharge: ko.observable(false),
    commercial: ko.observable(false),
    location: ko.observable(false),
    company: ko.observable(false)
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
      'eccoeccoeccopiva': ko.observable(''),
      'website': ko.observable(''),
      'phone': ko.observable(''),
      'email': ko.observable(''),
      'tag_list': ko.observable(''),
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

  self.edit_location_buffer =  {
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
      'Role': ko.observable('Location'),
      'type': ko.observable('location')
    }

  self.locations = ko.observableArray([]);

  self.init = function() {
    if(!lpi.is_logged()) {
      lpi.redirect('#login');
    }

    self.show_section({slug: 'partnership'});
  }

  self.check_family = function(family) {
    var handles = self.active_subscriptions();
    var families = family.split(',');
    for(i in handles) {
      if(typeof handles[i].indexOf == 'function') {
        for(f in families) {
          if(handles[i].indexOf(families[f]) >= 0 ||
              families[f] == '*')
            return true;
        }
      }
    }

    return false;
  }

  self.observe_form = function(data) {
    for(type in self.profiles) {
      if(data[type]) {
        for(i in data[type]) {
          self.profiles[type][i](data[type][i]?data[type][i]:'');
        }
      }
    }

    for(i in data.locations) {
      var location = {};
      for(field in data.locations[i]) {
        var value = data.locations[i][field];

        location[field] = ko.observable(value)
      }

      console.log(location);

      self.locations.push(location)
    }
  }

  self.edit_profile = function(type) {
    var profile = self.profiles[type];
    self.edit[type](true);
  }

  self.abort_edit_profile = function(type) {
    console.log('aborting ' + type);
    self.edit[type](false);
  }

  self.new_location = function() {
    self.edit['location'](true);
  }

  self.edit_location = function(location) {
    for(i in location) {
      self.edit_location_buffer[i](location[i]());
    }
    self.edit['location'](true);
  }

  self.abort_edit_location = function() {
    for(i in self.edit_location_buffer) {
      if(typeof(self.edit_location_buffer[i]) == 'function')
        self.edit_location_buffer[i]('');
    }
    self.edit_location_buffer['Role']('Location');
    self.edit_location_buffer['type']('location');
    self.edit['location'](false);
  }

  self.submit_location = function() {
    var location = {};
    for(i in self.edit_location_buffer) {
      location[i] = self.edit_location_buffer[i]();
    }

    console.log(location);

    location.company = self.profiles.company.first_name()
    location.company_id = self.profiles.company.id()

    lpi.post('edit_profile', location, function(response) {
      console.log(response);
      self.edit[type](false);
    });

    if(location.id == '') {
      var location = {};

      for (i in self.edit_location_buffer) {
        location[i] = ko.observable(self.edit_location_buffer[i]());
      };

      console.log('pushing ' + location.first_name());

      self.locations.push(location);
    } else {
      var locations = self.locations()
      for(i = 0; i< locations.length;i++) {
        console.log(locations[i].id + ' === ' + location.id);
        if(typeof(locations[i].id) == 'function') {
          if(locations[i].id() == location.id) {
              for(j in locations[i]) {
                if(typeof(locations[i][j]) == 'function')
                  locations[i][j](location[j]);
              }          
          }
        }
      }

      self.locations([]);
      self.locations(locations);
    }

    self.abort_edit_location();
  }

  self.add_tag = function(tag) {
    var tags = self.profiles.company.tag_list().split(",");
    tags.push(tag);
    self.profiles.company.tag_list(tags.join(","));
  }

  self.del_tag = function(tag) {
    var tags = self.profiles.company.tag_list().split(",");
    tags.splice(tags.indexOf(tag), 1);
    self.profiles.company.tag_list(tags.join(","));
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
        
        console.log(self.profiles.company.first_name());

      } else {
        lpi.request('account_info', {section: 'partnership'}, function(response) {
          self.ready['partnership'](response);
        });
      }
    },

    account: function(data) {
      self.management_url(data.url);
    }
  }

  self.show_section = function(section, data) {
    console.log('showing ' + section.slug + ' data ' + data);
    self.loading(true);
    lpi.loading(true);

    lpi.request('account_info', {section: section.slug, data: data}, function(response) {
      if(self.ready[section.slug]) {
        self.ready[section.slug](response.data);
      }

      self.loading(false);
      lpi.loading(false);
      self.active_section(section.slug);
    });
  }
}