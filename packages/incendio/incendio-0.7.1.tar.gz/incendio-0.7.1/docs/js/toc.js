// https://github.com/ghiculescu/jekyll-table-of-contents
// this library modified by fastai to:
// - update the location.href with the correct anchor when a toc item is clicked on
(function($){
  $.fn.toc = function(options) {
    var defaults = {
      noBackToTopLinks: false,
      title: '',
      minimumHeaders: 3,
      headers: 'h1, h2, h3, h4',
      listType: 'ol', // values: [ol|ul]
      showEffect: 'show', // values: [show|slideDown|fadeIn|none]
      showSpeed: 'slow' // set to 0 to deactivate effect
    },
    settings = $.extend(defaults, options);

    var headers = $(settings.headers).filter(function() {
      // get all headers with an ID
      var previousSiblingName = $(this).prev().attr( "name" );
      if (!this.id && previousSiblingName) {
        this.id = $(this).attr( "id", previousSiblingName.replace(/\./g, "-") );
      }
      return this.id;
    }), output = $(this);
    if (!headers.length || headers.length < settings.minimumHeaders || !output.length) {
      return;
    }

    if (0 === settings.showSpeed) {
      settings.showEffect = 'none';
    }

    var render = {
      show: function() { output.hide().html(html).show(settings.showSpeed); },
      slideDown: function() { output.hide().html(html).slideDown(settings.showSpeed); },
      fadeIn: function() { output.hide().html(html).fadeIn(settings.showSpeed); },
      none: function() { output.html(html); }
    };

    var get_level = function(ele) { return parseInt(ele.nodeName.replace("H", ""), 10); }
    var highest_level = headers.map(function(_, ele) { return get_level(ele); }).get().sort()[0];
    //var return_to_top = '<i class="glyphicon glyphicon-upload back-to-top"></i>';
    // other nice icons that can be used instead: glyphicon-upload glyphicon-hand-up glyphicon-chevron-up glyphicon-menu-up glyphicon-triangle-top
    var level = get_level(headers[0]),
      this_level,
      html = settings.title + " <"+settings.listType+">";
    headers.on('click', function() {
      if (!settings.noBackToTopLinks) {
        var pos = $(window).scrollTop();
        window.location.hash = this.id;
        $(window).scrollTop(pos);
      }
    })
    .addClass('clickable-header')
    .each(function(_, header) {
      base_url = window.location.href;
      base_url = base_url.replace(/#.*$/, "");
      this_level = get_level(header);
      //if (!settings.noBackToTopLinks && this_level > 1) {
      //  $(header).addClass('top-level-header').before(return_to_top);
      //}
      txt = header.textContent.split('¶')[0].split(/\[(test|source)\]/)[0];
      if (!txt) {return;}
      if (this_level === level) // same level as before; same indenting
        html += "<li><a href='" + base_url + "#" + header.id + "'>" + txt + "</a>";
      else if (this_level <= level){ // higher level than before; end parent ol
        for(i = this_level; i < level; i++) {
          html += "</li></"+settings.listType+">"
        }
        html += "<li><a href='" + base_url + "#" + header.id + "'>" + txt + "</a>";
      }
      else if (this_level > level) { // lower level than before; expand the previous to contain a ol
        for(i = this_level; i > level; i--) {
          html += "<"+settings.listType+">"+((i-level == 2) ? "<li class=\"hide_content\">" : "<li>")
        }
        html += "<a href='" + base_url + "#" + header.id + "'>" + txt + "</a>";
      }
      level = this_level; // update for the next one
    });
    html += "</"+settings.listType+">";
    if (!settings.noBackToTopLinks) {
      $(document).on('click', '.back-to-top', function() {
        $(window).scrollTop(0);
        window.location.hash = '';
      });
    }

    render[settings.showEffect]();
  };
})(jQuery);
