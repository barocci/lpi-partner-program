var geoplanet = {
  options: {
    'apiurl': 'http://where.yahooapis.com/v1/places.',
    'appid': 'dj0yJmk9OVpFcHJVTUw0VWVyJmQ9WVdrOVVHZDRSVFZDTm04bWNHbzlNVGN4TWpjME1qRTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD01ZQ--',
    'type': 7, // cities
    'count': 10,
  },

  map: {},

  search_cities: function(text, process) {
    var url = geoplanet.options.apiurl + "q('" + text + "%2A')";
    url += ";count=" + geoplanet.options.count;
    url += ";type=" + geoplanet.options.type;
    url += "?format=json";
    url += "&appid=" + geoplanet.options.appid;

    $.get(url, function(data) {
      geoplanet.results = data;
      var places_string = [];
      $.each(data.places.place, function(index) {
        var string = this.name + " (" +this.country+")";
        geoplanet.map[string] = this;
        places_string.push(string);
      });
      process(places_string);
    });
  },

  matcher: function(item) {
    if (item.toLowerCase().indexOf(this.query.trim().toLowerCase()) != -1) {
        return true;
    }
  },

  sorter: function(items) {
    return items.sort();
  },

  updater: function(input, key) {
    var prefix = $(input).data('prefix');
    var item = geoplanet.map[key];
    $('#' + prefix + '_lat').val(item.boundingBox.northEast.latitude);
    $('#' + prefix + '_lon').val(item.boundingBox.northEast.longitude);
    $('#' + prefix + '_woeid').val(item.woeid);

    return key;
  },

  highlighter: function(item) {
    var regex = new RegExp( '(' + this.query + ')', 'gi' );
    return item.replace( regex, "<strong>$1</strong>" );
  }
}
