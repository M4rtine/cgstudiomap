// ref : https://output.jsbin.com/quvelo/2/#tab3 
// fonction de re-formatage de l'adresse URL pour pouvoir accéder aux tabs depuis un lien et une page externe.



$(window).load(function () {

 	// cache the id
 	var navbox = $('.nav-tabs');

 	// activate tab on click
 	navbox.on('click', 'a', function (e) {
 		var $this = $(this);
 		// prevent the Default behavior
 		e.preventDefault();
 		// send the hash to the address bar
 		window.location.hash = $this.attr('href');
 		// activate the clicked tab
 		$this.tab('show');
 	});

 	// will show tab based on hash
 	function refreshHash() {
 		navbox.find('a[href="' + window.location.hash + '"]').tab('show');
 	}

 	// show tab if hash changes in address bar
 	$(window).bind('hashchange', refreshHash);

 	// read has from address bar and show it
 	if (window.location.hash) {
 		// show tab on load
 		refreshHash();
 	}

 });
