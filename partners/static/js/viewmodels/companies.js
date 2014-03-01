var CompaniesListViewModel = function() {
	var self = this;
	ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'companies';

  self.companies = ko.observableArray([]);
  self.cities = ko.observableArray([]);
  self.tags = ko.observableArray([]);
  self.active_tags = ko.observableArray([]);

  self.init = function() {
    lpi.request('search', {type: 'services'}, function(response) {
      self.update(response.data);
    });
    console.log(self.active_tags);
  };

  self.add_tag_filter = function(tag) {
    if(!self.tag_is_active(tag)) {
      var tags = self.active_tags();
      tags.push(tag);
      self.active_tags(tags);
    }
  };

  self.del_tag_filter = function(tag) {
    if(self.tag_is_active(tag)) {
      var tags = self.active_tags();
      console.log('rem: ' + tag);
      console.log('rem: ' + tags.indexOf(tag));
      tags.splice(tags.indexOf(tag), 1);
      console.log(tags);
      self.active_tags(tags);
    }
  };

  self.filter = function(tag) {
    console.log('filtering: ' +tag );
    if(self.tag_is_active(tag)) {
      self.del_tag_filter(tag);
    } else {
      self.add_tag_filter(tag);
    }

    self.filter_items();

    console.log(self.active_tags());
  };

  self.filter_items = function() {
    var contacts = self.companies();
    for(i in contacts) {
      var contact = contacts[i];
      console.log('considering ' + contacts[i].first_name);
      if(self.match_filters(contacts[i])) {
        console.log('showing: ' + contacts[i].first_name);
        contact.visible(true);
      } else {
        console.log('hiding: ' + contacts[i].first_name);
        contact.visible(false);
      }
    }
  };

  self.match_filters = function(contact) {
    var check_city = false;
    var check_tag = false;
    var active_tags = self.active_tags();

    if(active_tags.length == 0) {
      check_tag = check_city = true;
    } else {

      if(contact.tag_list) {
        var tags = contact.tag_list.split(',');
        for(i in tags) {
          if(active_tags.indexOf(tags[i]) >= 0) {
            check_tag = true;
          }
        }
      } 

      if(contact.city != '') {
        if(active_tags.indexOf(contact.city) >= 0) {
          check_city = true;
        }
      }
    }

    if(!check_city) {
      var cities = self.cities()
      var flag = false;
      for(i in cities) {
        if(self.active_tags().indexOf(cities[i]) >= 0) {
           flag = true;
        }
      }

      check_city = !flag;
    } 

    if(!check_tag) {
      var tags = self.tags()
      var flag = false;
      for(i in tags) {
        if(self.active_tags().indexOf(tags[i]) >= 0) {
           flag = true;
        }
      }

      check_tag = !flag;
    }

    return check_tag && check_city;
  }

  self.tag_is_active = function(tag) {
    var tags =  self.active_tags()
    return tags.indexOf(tag) >= 0;
  };

  self.update = function(data) {
    self.tags([]);
    
    for(i in data) {

      if(data[i].tag_list) {
        var tags = data[i].tag_list.split(',');
        self.tags(tags.unique(self.tags()));
      }

      if(data[i].city) {
        var city = data[i].city;
        var cities = self.cities();
        if(cities.indexOf(city) < 0) {
          cities.push(city);
        }

        self.cities(cities);
      }
      console.log(self.cities());
      
      data[i].visible = ko.observable(true);
    }
    
    console.log(self.tags());
    self.companies(data);
  };
}