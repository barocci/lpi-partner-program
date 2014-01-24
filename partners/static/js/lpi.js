var lpi = {
  valid_pages: ['intro', 'training', 'companies', 'joinus','signup', 'login', 'wizard', 'offers'],
  selected_page: 'intro',
  pages: {},

  init: function() {
    this.init_views();
    this.init_router(); 
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
      $('.lpi-layer').addClass(animations);
    } else {
      $('.lpi-layer').removeClass(animations);
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

