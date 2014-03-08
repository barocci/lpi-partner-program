var lpi = {
  valid_pages: ['intro', 'training', 'companies', 'joinus', 'teachers', 'academies',
                'signup', 'login', 'wizard', 'offers', 'account', 'info'],
  selected_page: 'intro',
  pages: {},

  username: '',
  user_id: '',

  tags: { option: 'PHP', 
          option: 'Python',
          option: 'Web Servers',
          option: 'Sysadmin',
          option: 'Javascript',
          option: 'Web'},


  init: function() {
    this.init_views();
    this.init_router(); 
    this.authenticate();
  },

  authenticate: function() {
    if(this.is_logged()) {
      console.log('is logged');
      if(this.username == '' || this.user_id == '') {
        var that = this;
        this.request('user_info',{}, function(response) {
          that.login(response);
        });
      }
      this.pages.nav.login();
    } else {
      console.log('not logged');
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
    console.log($.cookie('csrftoken'));
    if($.cookie('csrftoken') != undefined && 
       $.cookie('csrftoken') != '')
      return true;

    return false;
  },

  routing: false,

  init_router: function() {
    var that = this;

    function route(page, args) {
      console.log('Page sel' + that.selected_page);
      console.log('Page ' + page);
      if(that.routing) {
        console.log('redirecting ' + page);  
        that.redirect(that.selected_page);
        return;
      }

      if(that.valid_pages.indexOf(page) >= 0) {
        that.routing = true;
        var different = that.selected_page != page;
        var old_view = that.pages[that.selected_page];
        that.selected_page = page;
        var new_view = that.pages[page];

        if(!lpi.is_logged() && new_view.require_login) {
          console.log('redirecting');
          that.redirect('#login');
          return;
        }

        that.loading(true);

        function init_new_page() {
          that.pages.nav.set_page(page);
          old_view.end(page, args);
          new_view.init(args);

          if(different) {
            old_view.out_transition(function() {
                new_view.in_transition();
                that.loading(false);
                that.routing = false;
            });
          } else {
            new_view.in_transition();
            that.loading(false);
            that.routing = false;
          }

          $('body,html').animate({scrollTop: 0}, 500);
        }

        if(!new_view.template_loaded) {
          $.get('template',{id: new_view.template}, function(response) {
            $('.prtn-page-' + new_view.template).html(response);
            ko.applyBindings(new_view, $('.prtn-page-' + new_view.template)[0]);
            new_view.template_loaded = true;
            init_new_page();
          })
        } else {
          init_new_page();
        }
      }
    }

    routie({ 
       'info/:id': function(id) {
         route('info', {id: id});
       },
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
    //ko.applyBindings(this.pages.training, $('.prtn-page-training')[0]);
  
    // companies view
    this.pages.companies = new CompaniesListViewModel();
    //ko.applyBindings(this.pages.companies, $('.prtn-page-companies')[0]);

    // companies view
    this.pages.academies = new AcademiesListViewModel();
    ko.a//pplyBindings(this.pages.academies, $('.prtn-page-academies')[0]);

    // teachers view
    this.pages.teachers = new TeachersListViewModel();
    //ko.applyBindings(this.pages.teachers, $('.prtn-page-teachers')[0]);

    // joinus view
    this.pages.joinus = new JoinusViewModel();
    //ko.applyBindings(this.pages.joinus, $('.prtn-page-joinus')[0]);

    // offers view
    this.pages.offers = new OffersViewModel();
    //ko.applyBindings(this.pages.offers, $('.prtn-page-offers')[0]);

    // signup view
    this.pages.signup = new SignupViewModel();
    //ko.applyBindings(this.pages.signup, $('.prtn-page-signup')[0]);

    // info view
    this.pages.info = new InfoViewModel();
    //ko.applyBindings(this.pages.info, $('.prtn-page-info')[0]);

    // login view
    this.pages.login = new LoginViewModel();
    //ko.applyBindings(this.pages.login, $('.prtn-page-login')[0]);

    // wizard view
    this.pages.wizard = new WizardViewModel();
   // ko.applyBindings(this.pages.wizard, $('.prtn-page-wizard')[0]);

    // account view
    this.pages.account = new AccountViewModel();
    //ko.applyBindings(this.pages.account, $('.prtn-page-account')[0]);
  },

  request: function(method, params, callback) {
    $.getJSON('http://partners.lpi-italia.org/' + method + '/', params, function(response) {
        if(response.redirect) {
            lpi.redirect(response.redirect);
        }else {
            callback(response);
        }
     });
  },

  post: function(method, params, callback) {
    params['csrfmiddlewaretoken'] = $.cookie('csrftoken');
    $.post('http://partners.lpi-italia.org/' + method + '/', params, function(response) {
        console.log(response);
        if(response.redirect) {
            lpi.redirect(response.redirect);
        }else {
            callback(response);
        }
     });
  }


}


// Array Remove - By John Resig (MIT Licensed)
Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

Array.prototype.unique = function() {
    var a = this.concat();
    for(var i=0; i<a.length; ++i) {
        for(var j=i+1; j<a.length; ++j) {
            if(a[i] === a[j])
                a.splice(j--, 1);
        }
    }

    return a;
};