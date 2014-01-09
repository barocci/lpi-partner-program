var TrainingListViewModel = function() {
	var self = this;
	ko.BaseViewModel.call(self);

  self.trainers = ko.observableArray([])

	self.in_transition = function() {
    console.log('requesting');
    self.selected("prtn-page-selected");

		lpi.request('search', {Tipo: 'Trainer'}, function(data) {
      console.log(data);
      self.trainers(data);
		});
	}
}