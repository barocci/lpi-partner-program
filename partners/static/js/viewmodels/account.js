var AccountViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.tags = { option: 'PHP', 
                option: 'Python',
                option: 'Web Servers',
                option: 'Sysadmin',
                option: 'Javascript',
                option: 'Web'};

  self.require_login = true;

  self.sections = [{name: 'Partnership', slug: 'partnership', visible: true},
                   {name: 'Azienda', slug: 'profile', visible: true}, 
                   {name: 'Sedi operative', slug: 'locations', visible: true}, 
                   {name: 'Insegnanti', slug: 'teachers', visible: true}, 
                   {name: 'Account', slug: 'account', visible: true},
                   //{name: 'Pagamenti', slug: 'billing', visible: true}
                   ];


  self.active_section = ko.observable('');

  self.training = ko.observableArray([]);
  self.services = ko.observableArray([]);
  self.academic = ko.observableArray([]);

  self.loading = ko.observable(true);

  self.management_url = ko.observable('');


  self.selected_profile = ko.observable(false);
  self.profile_product = ko.observable(false);

  self.edit = { 
    incharge: ko.observable(false),
    commercial: ko.observable(false),
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
      'piva': ko.observable(''),
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
        $('#tags').tagsInput({
            'autocomplete': self.tags,
            'interactive':true,
            'width':'100%',
            'onAddTag':self.add_tag,
            'onRemoveTag':self.del_tag,
        });
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