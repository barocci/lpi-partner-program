var NavViewModel = function() {
  var self = this;
  ko.BaseViewModel.call(self);
  self.pages = ko.observable([{hash:'http://www.lpi-italia.org', label:'Home'},
                              {hash:'#training', label:'Formazione'},
                              {hash:'#companies', label:'Servizi e Soluzioni'},
                              {hash:'#academies', label:'Scuole e Universit&agrave;'},
                              //{hash:'joinus', label:'Partnership'},
                             // {hash:'teachers', label:'Docenti'}
                             ]);

  self.selected = ko.observable('intro');

  self.username = ko.observable('');

  self.logged = ko.observable(false);

  self.intro = ko.observable();

  self.login = function() {
    console.log(lpi);
    self.username(lpi.username);
    self.logged(true);
  };

  self.logout = function() {
    self.logged(false);
    lpi.request('logout',{}, function(response) {
      lpi.logout();
    });
  };

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