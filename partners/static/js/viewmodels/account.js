var AccountViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'account';

  self.init_edit_location = false;


  self.tags = [ 
                 'PHP', 
                 'Python',
                 'Web Servers',
                 'Sysadmin',
                 'Javascript',
                 'Web'
              ];

  self.require_login = true;

  self.old_password = ko.observable('');
  self.new_password = ko.observable('');
  self.new_password_conf = ko.observable('');
  self.pwd_error_message = ko.observable('');

  
  self.sections = [{name: 'Partnership', slug: 'partnership', visible: '*'},
                   {name: 'Azienda', slug: 'profile', visible: 'hidden'}, 
                   {name: 'Profilo', slug: 'profile', visible: 'ct'}, 
                   {name: 'Loghi', slug: 'logos', visible: '*'}, 
                   {name: 'Account', slug: 'account', visible: '*'},
                   {name: 'Pagamenti', slug: 'billing', visible: '*'}, 
                   ];


  self.active_section = ko.observable('');
  self.active_menu = ko.observable('');

  self.training  = ko.observableArray([]);
  self.services = ko.observableArray([]);
  self.academic = ko.observableArray([]);
  self.teachers = ko.observableArray([]);
  self.certified_teachers = ko.observableArray([]);

  self.state_label = function(state) {
    var labels = {
      'incomplete': 'Profilo incompleto.',
      'approving': 'In attesa di approvazione',
      'pending': 'In attesa di pagamento',
      'active': 'Attivo',
      'suspendend': 'Partnership sospesa',
      'closed': 'Partnership chiusa'
    }

    return labels[state];
  }

  self.active_subscriptions = ko.computed(function() {
    var subs = [];
    subs = subs.concat(self.training());
    subs = subs.concat(self.services());
    subs = subs.concat(self.academic());
    subs = subs.concat(self.certified_teachers());

    return subs
  });


  self.get_subscription = function(id) {
    var subs = self.active_subscriptions();
    var ret = false;

    subs.map(function(sub) {
      if(sub.id == id) {
        ret = sub;
      }
    });

    return ret;
  }

  self.active_products = ko.computed(function() {
    var products = [];
    var subs = self.active_subscriptions();
    console.log(subs);
    subs.map(function(sub) {
      if(sub.product) {
        products.push(sub.product.handle);
      }
    });

    return products;
  });

  self.active_logos = ko.computed(function() {
    var products = [];
    var subs = [];
    subs = subs.concat(self.training());
    subs = subs.concat(self.services());
    subs = subs.concat(self.academic());

    for(i in subs) {
      if(subs[i].product) {
        products.push(subs[i].product.image_url);
      }
    }

    return products;
  });

  self.loading = ko.observable(true);

  self.management_url = ko.observable('');

  self.selected_info = ko.observable('');

  self.selected_profile = ko.observable(false);
  self.profile_product = ko.observable(false);
  self.profile_handle = ko.observable(false);
  self.selected_subscription = null;

  self.edit = { 
    incharge: ko.observable(false),
    commercial: ko.observable(false),
    location: ko.observable(false),
    teacher: ko.observable(false),
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
      'twitter': ko.observable(''),
      'googleplus': ko.observable(''),
      'facebook': ko.observable(''),
      'website': ko.observable(''),
      'phone': ko.observable(''),
      'email': ko.observable(''),
      'skype_name': ko.observable(''),
      'tag_list': ko.observable(''),
      'lat': ko.observable(''),
      'lng': ko.observable(''),
      'Verification': ko.observable(''),
      'LPICID': ko.observable(''),
      'LPICDate': ko.observable(''),
      'LPICLevel': ko.observable(''),
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
      'twitter': ko.observable(''),
      'googleplus': ko.observable(''),
      'facebook': ko.observable(''),
      'postcode': ko.observable(''),
      'country': ko.observable(''),
      'piva': ko.observable(''),
      'website': ko.observable(''),
      'skype_name': ko.observable(''),
      'phone': ko.observable(''),
      'email': ko.observable(''),
      'lat': ko.observable(''),
      'lng': ko.observable(''),
      'Verification': ko.observable(''),
      'LPICID': ko.observable(''),
      'LPICDate': ko.observable(''),
      'LPICLevel': ko.observable(''),
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
      'twitter': ko.observable(''),
      'googleplus': ko.observable(''),
      'facebook': ko.observable(''),
      'lat': ko.observable(''),
      'lng': ko.observable(''),
      'website': ko.observable(''),
      'skype_name': ko.observable(''),      
      'phone': ko.observable(''),
      'email': ko.observable(''),
      'Verification': ko.observable(''),
      'LPICID': ko.observable(''),
      'LPICDate': ko.observable(''),
      'LPICLevel': ko.observable(''),
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
      'twitter': ko.observable(''),
      'googleplus': ko.observable(''),
      'skype_name': ko.observable(''),
      'facebook': ko.observable(''),
      'image_url': ko.observable(''),
      'LPICID': ko.observable(''),
      'LPICDate': ko.observable(''),
      'LPICLevel': ko.observable(''),
      'lat': ko.observable(''),
      'lng': ko.observable(''),
      'company_id': ko.observable(''),
      'Role': ko.observable('Location'),
      'type': ko.observable('location')
    }

  self.edit_teacher_buffer =  {
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
      'twitter': ko.observable(''),
      'googleplus': ko.observable(''),
      'skype_name': ko.observable(''),
      'LPICID': ko.observable(''),
      'LPICDate': ko.observable(''),
      'LPICLevel': ko.observable(''),
      'facebook': ko.observable(''),
      'image_url': ko.observable(''),
      'lat': ko.observable(''),
      'lng': ko.observable(''),
      'company_id': ko.observable(''),
      'Role': ko.observable('Teacher'),
      'type': ko.observable('teacher')
    }

  self.current_step = {
    'product': ko.observable(''),
    'contact': ko.observable(''),
    'subscription': ko.observable(''),
    'incharge': ko.observable(0),
    'representative': ko.observable(0),
    'teachers': ko.observable(0),
    'location': ko.observable(0),
    'billing': ko.observable(0),
    'book': ko.observable(0),
    'completed': ko.observable(0),
  }

  self.locations = ko.observableArray([]);
  self.teachers = ko.observableArray([]);
  self.certified_teachers = ko.observableArray([]);

  self.initialized = false;

  self.init = function(params) {
    if(!lpi.is_logged()) {
      lpi.redirect('#login');
    }

    console.log('initializing map');
    console.log(params);

    self.active_section('');
    
    function goto_section() {
      if(params != undefined && params.section != undefined) {
        if(params.id != undefined) {
          self.show_section({slug: params.section}, params.id);
        } else {
          self.show_section({slug: params.section});
        }

      } else {
        self.show_section({slug: 'partnership'});
      }
    }

    if(!self.initialized) {
      lpi.request('account_info', {section: 'init'}, function(response) {
        console.log(response);
        self.training(response.data.training);
        self.services(response.data.services);
        self.academic(response.data.academic);
        self.teachers(response.data.teachers);
        self.certified_teachers(response.data.certified_teachers);
        self.initialized = true;
        goto_section();
      });
    } else {
      goto_section();
    }

  }

  self.end = function() {
    self.initialized = false;
  }


       
  self.open_instructions = function(deal) {
    self.selected_info(deal.id);
    console.log(deal);
  }

  self.check_family = function(family, set) {
    var handles;

    if(set != undefined) {
      handles = set;
    } else {
      handles = self.active_products();
    }

    console.log(handles);
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

  self.profile_family = function() {
    var family = '';
    if(self.profile_handle()) {
      var parts = self.profile_handle().split('-');
      if(parts.length > 1) {
        family = parts[1];
      }
    }

    return family;
  }

  self.observe_form = function(data) {
    for(type in self.profiles) {
      if(data[type]) {
        for(i in data[type]) {
          self.profiles[type][i](data[type][i]?data[type][i]:'');
        }
      }
    }

    self.teachers([]);
    console.log(data);
    for(i =0; i < data.teachers.length; i++) {
      var teacher = {};
      console.log(i);
      console.log(data.teachers[i]);

      for(field in data.teachers[i]) {
        var value = data.teachers[i][field];

        teacher[field] = ko.observable(value)
      }

      console.log(teacher);

      self.teachers.push(teacher);
    }
    

    self.locations([]);
    for(i =0; i < data.locations.length; i++) {
      var location = {};
      for(field in data.locations[i]) {
        var value = data.locations[i][field];

        location[field] = ko.observable(value)
      }

      console.log(location);

      self.locations.push(location);
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

    if(!self.init_edit_location) {
    console.log('edit location ' + $('.address_picker', '.location_content').length);

      $('.address_picker', '.location_content').geocomplete({
        map: '.address_map',
        details: '.address_details'
      }).bind("geocode:result", function(event, result) {
        console.log(result);
        $('input', '.address_details').trigger('change');
        var steet = '';
        var street_number = '';

        result.address_components.map(function(item) {
          if(item.types.indexOf('route') >= 0) {
            street = item.long_name;
            console.log('set street ' + street);
          }

          if(item.types.indexOf('street_number') >= 0) {
            street_number = item.long_name;
          }

          if(item.types.indexOf('locality') >= 0) {
            self.edit_location_buffer.city(item.long_name);
          }

          if(item.types.indexOf('country') >= 0) {
            self.edit_location_buffer.country(item.long_name);
          }

          if(item.types.indexOf('postal_code') >= 0) {
            self.edit_location_buffer.postcode(item.long_name);
          }

        });

        console.log('street -> ' + street);
        self.edit_location_buffer.street(street + ' ' + street_number);
        self.edit_location_buffer.lat(result.geometry.location['k']);
        self.edit_location_buffer.lng(result.geometry.location['A']);
        
      });
      self.init_edit_location = true;
    }
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
    location.sub = self.selected_profile()
    location.handle = self.profile_handle();
    lpi.post('edit_profile', location, function(response) {
      console.log(response);
      self.edit[type](false);
      self.update_step(response.data.step);
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

  self.step_completed = function(step) {
    var ret = true;
    console.log(step);
    for(i in step) {
      if(step[i] == 0) {
        console.log('STEP NOT FINISHED');
        ret = false;
      }
    }

    return ret;
  }

  self.update_step = function(step) {
    console.log(step);
    for(i in step) {
      console.log(i);
      self.current_step[i](step[i]);
    }

    var sub = self.get_subscription(self.selected_profile());
    console.log(step);

    if(sub.state == 'incomplete' && step.completed) {
      self.initialized = false;
      
      lpi.alert("Il tuo profilo e' completo.<br>Torna alla "+ 
                "<a href='#account/partnership'>partnership</a> per il prossimo step.");

    }
  }

  self.new_teacher = function() {
    self.edit['teacher'](true);
  }

  self.edit_teacher = function(teacher) {
    for(i in teacher) {
      self.edit_teacher_buffer[i](teacher[i]());
    }
    self.edit['teacher'](true);
  }

  self.abort_edit_teacher = function() {
    for(i in self.edit_teacher_buffer) {
      if(typeof(self.edit_teacher_buffer[i]) == 'function')
        self.edit_teacher_buffer[i]('');
    }
    self.edit_teacher_buffer['Role']('Teacher');
    self.edit_teacher_buffer['type']('teacher');
    self.edit['teacher'](false);
  }

  self.submit_teacher = function() {
    var teacher = {};
    for(i in self.edit_teacher_buffer) {
      teacher[i] = self.edit_teacher_buffer[i]();
    }

    console.log(teacher);

    teacher.company = self.profiles.company.first_name();
    teacher.company_id = self.profiles.company.id();
    teacher.sub = self.selected_profile();
    teacher.handle = self.profile_handle();
    lpi.post('edit_profile', teacher, function(response) {
      console.log(response);
      self.edit[type](false);
      self.update_step(response.data.step);
    });

    if(teacher.id == '') {
      var teacher = {};

      for (i in self.edit_teacher_buffer) {
        teacher[i] = ko.observable(self.edit_teacher_buffer[i]());
      };

      console.log('pushing ' + teacher.first_name());

      self.teachers.push(teacher);
    } else {
      var teachers = self.teachers()
      for(i = 0; i< teachers.length;i++) {
        console.log(teachers[i].id + ' === ' + teacher.id);
        if(typeof(teachers[i].id) == 'function') {
          if(teachers[i].id() == teacher.id) {
              for(j in teachers[i]) {
                if(typeof(teachers[i][j]) == 'function')
                  teachers[i][j](teacher[j]);
              }          
          }
        }
      }

      self.teachers([]);
      self.teachers(teachers);
    }

    self.abort_edit_teacher();
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

  self.tags = function() {
    var tags = self.profiles.company.tag_list().split(',');
    tags.map(function(tag, index) {
      tags[index] = tag.trim();
    });
    return tags;
  }

  self.submit_profile = function(type) {
    var profile = ko.mapping.toJS(self.profiles[type]);
    profile.company = self.profiles.company.first_name()
    profile.company_id = self.profiles.company.id()
    profile.sub = self.selected_profile()
    profile.handle = self.profile_handle()
    lpi.post('edit_profile', profile, function(response) {
      self.edit[type](false);
      self.update_step(response.data.step);
      lpi.alert('Profilo aggiornato correttamente.')
    });
  }

  self.goto_profile = function(obj) {
    console.log('Going to profile');
    console.log(obj);
    self.selected_subscription = obj;
    self.selected_profile(obj.id);
    self.profile_product(obj.product.name);
    self.profile_handle(obj.product.handle);
    lpi.redirect('account/profile/' + obj.id);
  }

  self.show_all_profiles = function() {
    self.selected_profile(false);
    self.profile_product(false);
    self.ready['profile']();
  }

  self.redirect = function(slug) {
    self.active_menu(slug);
    lpi.redirect("account/" + slug);
  };

  self.is_newbie = ko.computed(function() {
    var count = self.training().length + self.services().length + self.academic().length;
    return count == 1;
  });

  self.ready = {
    profile: function(response) {
      var data = response.data;
      console.log(data);

      if(data.subscription) {
        self.selected_profile(data.subscription.id);
        self.profile_product(data.subscription.product);
        self.profile_handle(data.subscription.product);
        self.update_step(data.step);
      }

      if(self.selected_profile()) {
        self.observe_form(data);
        $('#tag_select').chosen({
          max_selected_options: 5,
          width:'100%'
        });

        $('#tag_select').on('change', function(evt, params) {
          self.profiles.company.tag_list($('#tag_select').val().join(','));
          self.submit_profile('company'); 
        });

        $('#fileupload').fileupload({
              dataType: 'json',
              done: function (e, data) {
                $('.avatar-box img').attr('src', data.result.url);
              }
        });
      } else {
       // lpi.request('account_info', {section: 'partnership'}, function(response) {
       //   self.ready['partnership'](response);
       // });
      }
    },

    billing: function(response) {
      if(response.error == 1) {
        self.management_url(false);
      } else {
        self.management_url(response.data.url);
      }
    }
  }

  self.show_section = function(section, data) {
    console.log(data);
    console.log('showing ' + section.slug + ' data ' + data);
    self.loading(true);
    lpi.loading(true);

    self.active_menu(section.slug);
    if(self.ready[section.slug] != undefined) {
      console.log('ajaxing');
      lpi.request('account_info', {section: section.slug, data: data}, function(response) {
        self.ready[section.slug](response);
        self.loading(false);
        lpi.loading(false);
        self.active_section(section.slug);
      });
    } else {
      self.loading(false);
      lpi.loading(false);
      self.active_section(section.slug);
    }
  }

  self.change_password = function() {
    if(self.new_password() ==  '' || self.new_password_conf() == '') {
      self.pwd_error_message("La nuova password non puo' essere vuota.")
    } else if(self.new_password() != self.new_password_conf()) {
      self.pwd_error_message('Le password non combaciano.')
    } else {
      console.log('changing password');
      lpi.post('change_password', 
               { new_password: self.new_password(),
                 old_password: self.old_password()}, 
                 function(response) {

        self.new_password('');
        self.new_password_conf('');
        self.old_password('');

        if(response.error != 1) {
          self.pwd_error_message('Password aggiornata.');
          setTimeout(function(){ self.pwd_error_message('')}, 4000);
        } else {
          self.pwd_error_message(response.data);
        }
      });
    }
  }
}
