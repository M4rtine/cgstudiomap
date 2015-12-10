(function($){

	function loadSVG(svgId, svgFile) {
		Snap.load(svgFile, function (f) {	
			var svg = Snap(svgId);
			svg.append(f);
		});
	}
	
	$(document).ready(function() {


		// Nav
        loadSVG("#arrow-down", "/shared_web_theme/static/src/svg/__arrow-down.svg");
        loadSVG("#logo-nav", "/shared_web_theme/static/src/svg/__logo-nav.svg");
        loadSVG("#user-login", "/shared_web_theme/static/src/svg/__user-login.svg");
        loadSVG("#toggle", "/shared_web_theme/static/src/svg/__toggle.svg");
        
        // Stats
        $(".stats div").each(function( index ) {
            loadSVG(this, "/shared_web_theme/static/src/svg/__stats-bg.svg");
         });
        
        // Socials
/*        loadSVG("#gitub-svg", "/shared_web_theme/static/src/svg/__social-git.svg");
        loadSVG("#twitter-svg", "/shared_web_theme/static/src/svg/__social-twitter.svg");
        loadSVG("#linkedin-svg", "/shared_web_theme/static/src/svg/__social-li.svg");*/

        $('.dropdown-toggle').dropdown();

		/* ---------------------------------------------- /*
		 * Smooth scroll / Scroll To Top
		/* ---------------------------------------------- */

		$('a[href*=#]').bind("click", function(e){
           
			var anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $(anchor.attr('href')).offset().top
			}, 1000);
			e.preventDefault();
		});

		$(window).scroll(function() {
			if ($(this).scrollTop() > 100) {
				$('.scroll-up').fadeIn();
			} else {
				$('.scroll-up').fadeOut();
			}
		});

	});

})(jQuery);
