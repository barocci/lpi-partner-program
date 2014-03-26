

var InfoViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'info';

  self.selected_company = ko.observable(-1);

  self.is_owner = ko.observable();
  self.changed = ko.observable(false);

  self.locations = ko.observableArray([]);

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
      'LPICID': ko.observable(''),
      'Verification': ko.observable(''),
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
      'LPICID': ko.observable(''),
      'Verification': ko.observable(''),
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
      'LPICID': ko.observable(''),
      'Verification': ko.observable(''),
      'company_id': ko.observable(''),
      'Role': ko.observable('Commercial'),
      'type': 'commercial',
    }
  }

  self.teachers = ko.observableArray([]);
  self.locations = ko.observableArray([]);
  self.references = ko.observableArray([]);


  self.init = function(arg) {
    self.selected_company(arg.id);

    lpi.request('details', {id: arg.id}, function(response) {
      var data = response.data;
      console.log(data);
      self.is_owner(data.owner);




      for(type in self.profiles) {
        if(data[type]) {
          for(i in data[type]) {
            console.log(i);
            self.profiles[type][i](data[type][i]?data[type][i]:'');
          }
        }
      }

      var contacts = ['teachers', 'locations', 'references'];

      for(type = 0; type < contacts.length; type++) {
        for(i =0; i < data[contacts[type]].length; i++) {
          var contact_obs = {};
          var contact = data[contacts[type]][i];
          for(field in contact) {
            var value = contact[field];

            contact_obs[field] = ko.observable(value)
          }

          console.log(contact_obs);

          self[contacts[type]].push(contact_obs);
        }
      }
    });
  }

  self.end = function() {
    self.teachers([]);
    self.locations([]);
    self.references([]);

    for(type in self.profiles) {
          for(i in self.profiles[type]) {
            if(typeof(self.profiles[type][i]) == 'function') {
              self.profiles[type][i]('');
            }
          }
      }

  }

  self.tags = function() {
    console.log(self.profiles.company.tag_list());
    var tags = [];
    if(self.profiles.company.tag_list().length > 0 ) {
      tags = self.profiles.company.tag_list().split(',');
      console.log(tags);
      while(tags.indexOf("") >= 0) {
        tags = tags.remove(tags.indexOf(""));
      }
    }
    
    return tags;
  }
}