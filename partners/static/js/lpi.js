var lpi = {
  valid_pages: ['intro', 'training', 'companies', 'joinus',
                'signup', 'login', 'wizard', 'offers', 'account'],
  selected_page: 'intro',
  pages: {},

  username: '',
  user_id: '',

  init: function() {
    this.init_views();
    this.init_router(); 
    this.authenticate();
  },

  authenticate: function() {
    if(this.is_logged()) {
      if(this.username == '' || this.user_id == '') {
        var that = this;
        this.request('user_info',{}, function(response) {
           that.login(response);
        });
      }
      this.pages.nav.login();
    } else {
      this.pages.nav.logout();
    }
  },

  login: function(user) {
    if(user) {
      this.username = user.username;
      this.user_id = user.user_id;
      this.authenticate();
    }
  },

  logout: function() {
    $.cookie('csrftoken', '');
    $.cookie('sessionid', '');
    this.username = this.user_id = '';
    this.redirect('#login');
  },

  is_logged: function() {
    if($.cookie('csrftoken') != '')
      return true;

    return false;
  },

  init_router: function() {
    var that = this;

    function route(page, args) {
      if(that.valid_pages.indexOf(page) >= 0) {
         var old_view = that.pages[that.selected_page];
         var new_view = that.pages[page];
         that.loading(true);
         that.pages.nav.set_page(page);
         old_view.end(page, args);
         new_view.init(args);

         if(page != that.selected_page) {
           old_view.out_transition(function() {
              that.selected_page = page;
              new_view.in_transition();
              that.loading(false);
           });
         } else {
           new_view.in_transition();
           that.loading(false);

         }

         $('body,html').animate({scrollTop: 0}, 500);
      }
    }

    routie({ 
       'offers/:type': function(type) {
         route('offers', {type: type});
       },
       'wizard/:id/:handle': function(id, handle) {
          route('wizard', {id: id, handle: handle});
       },

       'signup/:handle': function(handle) {
          route('signup', {handle: handle});
       },
       '*': route
    });

    if(window.location.hash == '') {
      routie('intro');
    }

  },

  loading: function(flag) {
    var animations = 'lpi-layer-active';
    if(flag) {
      $('.lpi-layer-image').addClass(animations);
    } else {
      $('.lpi-layer-image').removeClass(animations);
    }
  },

  redirect: function(path)  {
    routie(path);
  },

  store: function(key, value) {
    var store = locationStorage['lpi'];
    store[key] = value;
    localStorage['lpi'] = store;
    return value;
  },
  
  load: function(key) {
    var store = locationStorage['lpi'];
    return store[key];
  },

  init_views: function() {
    // nav view
    this.pages.nav = new NavViewModel();
    ko.applyBindings(this.pages.nav, $('#prtn-navbar')[0]);

    // intro view
    this.pages.intro = new IntroViewModel();
    ko.applyBindings(this.pages.intro, $('.prtn-page-intro')[0]);
    
    // training view
    this.pages.training = new TrainingListViewModel();
    ko.applyBindings(this.pages.training, $('.prtn-page-training')[0]);
  
    // companies view
    this.pages.companies = new CompaniesListViewModel();
    ko.applyBindings(this.pages.companies, $('.prtn-page-companies')[0]);

    // joinus view
    this.pages.joinus = new JoinusViewModel();
    ko.applyBindings(this.pages.joinus, $('.prtn-page-joinus')[0]);

    // offers view
    this.pages.offers = new OffersViewModel();
    ko.applyBindings(this.pages.offers, $('.prtn-page-offers')[0]);

    // signup view
    this.pages.signup = new SignupViewModel();
    ko.applyBindings(this.pages.signup, $('.prtn-page-signup')[0]);

    // login view
    this.pages.login = new LoginViewModel();
    ko.applyBindings(this.pages.login, $('.prtn-page-login')[0]);

    // wizard view
    this.pages.wizard = new WizardViewModel();
    ko.applyBindings(this.pages.wizard, $('.prtn-page-wizard')[0]);

    // account view
    this.pages.account = new AccountViewModel();
    ko.applyBindings(this.pages.account, $('.prtn-page-account')[0]);
  },

  request: function(method, params, callback) {
    $.getJSON('http://partners.lpi-italia.org/' + method + '/', params, function(response) {
        if(response.redirect) {
            lpi.redirect(response.redirect);
        }else {
            callback(response);
        }
     });
  }

}

