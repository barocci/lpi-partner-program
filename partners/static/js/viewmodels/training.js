var TrainingListViewModel = function() {
	var self = this;
	ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'training';

  self.trainers = ko.observableArray([])
  self.cities = ko.observableArray([]);
  self.tags = ko.observableArray([]);
  self.active_tags = ko.observableArray([]);

  self.init = function() {
    lpi.request('search', {type: 'training'}, function(response) {
      self.update(response.data);
    });
    console.log(self.active_tags);
  };

  self.partner_type = function(partner) {
    var mapping = {
      'lpi-atp': 'Approved Trining Partner',
      'lpi-atp-pro': 'Approved Training Partner PRO',
    }

    return mapping[partner.handle];
  };

  self.add_tag_filter = function(tag, type) {
    if(!self.tag_is_active(tag)) {
      var tags = self.active_tags();
      tags.push(tag.trim());
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
    var contacts = self.trainers();
    console.log(contacts);
    for(i in contacts) {
      var contact = contacts[i];

      console.log(contacts.length + ' - ' + i + ' - considering ' + contact.contact_name);
      
      if(self.match_filters(contacts[i])) {
        console.log('showing: ' + contact.contact_name);
        contact.visible(true);
      } else {
        console.log('hiding: ' + contact.contact_name);
        contact.visible(false);
      }

    }
  };

  self.match_filters = function(contact) {
    var check_city = false;
    var check_tag = false;

    var active_tags = self.active_tags();
    var tags = [];
    var cities = [];

    if(active_tags.length == 0) {
      check_tag = check_city = true;
    } else {
      if(contact.tags) {
        var tags = contact.tags.split(',');
        for(j=0; j < tags.length; j++) {
          tags[j] = tags[j].trim();
        }
      }

      if(contact.cities != '' && contact.cities != undefined) {
        var cities = contact.cities.split(',');
        for(j=0; j < cities.length; j++) {
          cities[j] = cities[j].trim();
        }
      }

      tags = tags.concat(cities);
      console.log(tags);

      if(tags.length > 0) {
        var counter = 0;
        for(i =0; i < active_tags.length; i++) {
          var check_tag = true;
          if(tags.indexOf(active_tags[i].trim()) >= 0) {
            counter++;
          }
        }

        check_tag = (counter == active_tags.length);
      } else {
        check_tag = false;
      }
    }


    return check_tag;// && check_city;
  }

  self.tag_is_active = function(tag) {
    var tags =  self.active_tags()
    return tags.indexOf(tag.trim()) >= 0;
  };

  self.update = function(data) {
    self.tags([]);
    
    for(i in data) {

      if(data[i].tags) {
        var tags = data[i].tags.split(',');
        for(j = 0; j < tags; j++) {
          tags[j] = tags[j].trim();
        }

        self.tags(tags.unique(self.tags()));
      }

      if(data[i].cities) {
        var city = data[i].cities.split(', ');
        var cities = self.cities();
        cities = city.unique(cities);
        console.log(city);
        console.log(cities);
        self.cities(cities);
      }
      
      data[i].visible = ko.observable(true);
    }


    self.trainers(data);
    $('.list-icon-image').tooltip({animation:true});
  };
}

  