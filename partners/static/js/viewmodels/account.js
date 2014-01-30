var AccountViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);

  self.init = function() {
    if(!lpi.is_logged()) {
      lpi.redirect('#login');
    }
  }
}