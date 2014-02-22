var TrainingListViewModel = function() {
	var self = this;
	ko.BaseViewModel.call(self);

  self.trainers = ko.observableArray([])

	self.in_transition = function() {
    console.log('requesting');
    self.selected("prtn-page-selected");

		lpi.request('search', {type: 'training'}, function(response) {
      self.trainers(response.data);
		});
	}
}