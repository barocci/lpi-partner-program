var OffersViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.template_loaded = false;
  self.template = 'teachers';

  self.products = ko.observableArray();
  self.type = ko.observable();
  self.show = ko.observable(false);

  self.product_low = { 
    'id': ko.observable(''),
    'name': ko.observable(''),
    'handle': ko.observable(''),
    'description': ko.observable(''),
    'price_in_cents': ko.observable(''),
  };

  self.product_middle = { 
    'id': ko.observable(''),
    'name': ko.observable(''),
    'handle': ko.observable(''),
    'description': ko.observable(''),
    'price_in_cents': ko.observable(''),
  };

  self.product_pro = { 
    'id': ko.observable(''),
    'name': ko.observable(''),
    'handle': ko.observable(''),
    'description': ko.observable(''),
    'price_in_cents': ko.observable(''),
  }

  self.init = function(param) {
    if(param == undefined) {
      lpi.redirect('joinus');
      return false;
    }
    self.type(param.type);

    self.show(true);
    return;
   
    lpi.request('load_products',{family: self.type()}, function(response) {
      var products = self.order_by_price(response);
      console.log(products);

      if(products.length > 0) {
        for(i in self.product_low) {
          console.log('setting '+i)
          self.product_low[i](products[0][i]);
        }
      }

      if(products.length > 1) {
        for(i in self.product_low) {
          self.product_middle[i](products[1][i]);
        }
      }

      if(products.length > 2) {
        for(i in self.product_low) {
          self.product_pro[i](products[2][i]);
        }
      }

      self.show(true);
    });
  };

  self.end = function() {
    self.show(false);
  };

  self.buy = function() {

  };

  self.order_by_price = function(products) {
    function compare(a, b) {
      if(a.price_in_cents < b.price_in_cents) 
        return -1;

      if(a.price_in_cents < b.price_in_cents) 
        return 1;

      return 0;
    }

    return products.sort(compare);
  };


}
