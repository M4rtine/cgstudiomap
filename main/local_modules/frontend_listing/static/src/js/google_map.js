/**
 * Script to manage the map displayed to list companies
 * Created by foutoucour on 12/10/15.
 * The theme of the map is loaded from `snazzy_theme.py` file.

 * CUSTOMS infos windows ref : http://en.marnoto.com/2014/09/5-formas-de-personalizar-infowindow.html
 */

function initialize(geoloc) {
    //To center map on markers
    var bounds = new google.maps.LatLngBounds();

    var mapCanvas = document.getElementById('map');
    var mapOptions = {
		minZoom: 3, 

        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false,
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        },
        scaleControl: true,
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.LEFT_CENTER
        }
    };
    var map = new google.maps.Map(mapCanvas, mapOptions);
    var markers = [];
    var icon = '/frontend_listing/static/src/marker.svg';
    var iconStudio = '/frontend_listing/static/src/marker-studio.svg';


    //INFOWINDOWS
    var infowindow = new google.maps.InfoWindow({
        //content: contentString,
        width: 300,
        maxWidth: 350
    });

    // This event expects a click on a marker
    // When this event is fired the Info Window is opened.
    //google.maps.event.addListener(marker, 'click', function () {
    //    infowindow.open(map, marker);
    //});

    // Event that closes the Info Window with a click on the map
    google.maps.event.addListener(map, 'click', function () {
        infowindow.close();
    });

    // *
    // START INFOWINDOW CUSTOMIZE.
    // The google.maps.event.addListener() event expects
    // the creation of the infowindow HTML structure 'domready'
    // and before the opening of the infowindow, defined styles are applied.
    // *
    google.maps.event.addListener(infowindow, 'domready', function () {
        // Reference to the DIV that wraps the bottom of infowindow
        var iwOuter = $('.gm-style-iw');

        /* Since this div is in a position prior to .gm-div style-iw.
         * We use jQuery and create a iwBackground variable,
         * and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
         */
        var iwBackground = iwOuter.prev();

        // Removes background shadow DIV
        iwBackground.children(':nth-child(2)').css({
            'display': 'none'
        });

        // Removes white background DIV
        iwBackground.children(':nth-child(4)').css({
            'display': 'none'
        });

        // Moves the infowindow 115px to the right.
        iwOuter.parent().parent().css({
            left: '115px'
        });

        // Moves the shadow of the arrow 76px to the left margin.
        iwBackground.children(':nth-child(1)').attr('style', function (i, s) {
            return s + 'left: 76px !important;'
        });

        // Moves the arrow 76px to the left margin.
        iwBackground.children(':nth-child(3)').attr('style', function (i, s) {
            return s + 'left: 76px !important;'
        });

        // Changes the desired tail shadow color.
        iwBackground.children(':nth-child(3)').find('div').children().css({
            'box-shadow': 'rgba(72, 181, 233, 0.6) 0px 1px 6px',
            'z-index': '1'
        });

        // Reference to the div that groups the close button elements.
        var iwCloseBtn = iwOuter.next();

        // Apply the desired effect to the close button
        iwCloseBtn.css({
            opacity: '1',
            right: '50px',
            top: '11px',
            backgroundColor: '#b05ae2'
        });

        // If the content of infowindow not exceed the set maximum height, then the gradient is removed.
        if ($('.iw-content').height() < 140) {
            $('.iw-bottom-gradient').css({
                display: 'none'
            });
        }

        // The API automatically applies 0.7 opacity to the button after the mouseout event. This function reverses this event to the desired value.
        iwCloseBtn.mouseout(function () {
            $(this).css({
                opacity: '1'
            });
        });
    });

    jQuery.each(geoloc, function (i, val) {
        var contentString = '<div id="content">' + val[2] + '</div>';

        var marker = new google.maps.Marker({
            position: {lat: val[0], lng: val[1]},
            map: map,
            icon: iconStudio,
            title: i
        });
        
        //extend the bounds to include each marker's position
        bounds.extend(marker.position);
        markers.push(marker);

        google.maps.event.addListener(marker, 'click', function () {
            infowindow.setContent(contentString);
            infowindow.open(map, marker);
        });

    });

    var clusterStyles = [
        {
            textColor: '#f1f1f3',
            url: icon,
            textSize: 18,
            height: 48,
            width: 48
        }
    ];

    var mcOptions = {
        gridSize: 50,
        styles: clusterStyles,
        maxZoom: 15
    };

    var mc = new MarkerClusterer(map, markers, mcOptions);
    //now fit the map to the newly inclusive bounds
    map.fitBounds(bounds);
    map.setOptions({styles: snazzy_theme()});
}
google.maps.event.addDomListener(window, 'load', initialize);