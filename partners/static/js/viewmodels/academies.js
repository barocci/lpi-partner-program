var AcademiesListViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);
  self.academies = ko.observableArray([])

  self.in_transition = function() {
    console.log('requesting');
    self.selected("prtn-page-selected");

    lpi.request('search', {type: 'academic'}, function(response) {
      self.academies(response.data);

    });
  }
}