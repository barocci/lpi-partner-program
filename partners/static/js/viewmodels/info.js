

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

  self.teachers = ko.observableArray([]);
  self.locations = ko.observableArray([]);


  self.init = function(arg) {
    self.selected_company(arg.id);

    lpi.request('details', {id: arg.id}, function(response) {
      var data = response.data;
      console.log(data);
      self.is_owner(data.owner);

      for(type in self.profiles) {
        if(data[type]) {
          for(i in data[type]) {
            console.log("Setting[" + type + "] " + i + " = " + data[type][i]);
            self.profiles[type][i](data[type][i]?data[type][i]:'');
          }
        }
      }
    });

  }
}