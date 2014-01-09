var CompaniesListViewModel = function() {
	var self = this;
	ko.BaseViewModel.call(self);
  self.companies = ko.observableArray([])

  self.in_transition = function() {
    console.log('requesting');
    self.selected("prtn-page-selected");

    lpi.request('search', {Tipo: 'Company'}, function(data) {
      self.companies(data);
    });
  }
}