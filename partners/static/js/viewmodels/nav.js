var NavViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);
  self.pages = ko.observable([{hash:'intro', label:'Home'},
                 {hash:'training', label:'Formazione'},
                 {hash:'companies', label:'Servizi'},
                 {hash:'joinus', label:'Partnership'},
                 {hash:'teachers', label:'Docenti'}]);

  self.selected = ko.observable('intro');

  self.intro = ko.observable();

  self.set_page = function(page) {
    var esclude = [
       'wizard',
       'signup',
       'offers',
       'login'
    ]
    if(esclude.indexOf(page) >= 0) return;
    self.selected(page);
  }


  
}