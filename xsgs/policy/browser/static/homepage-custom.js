require([
  'jquery','jqswfobj','ajax-fetchimg','bootstrap-carousel'
], function($,jqswf,ajaximg,carousel) {
  'use strict';
$(document).ready(function(){
		rolltext(".roll-wrapper");
		genswf("http://images.315ok.org/xsgs998/main.swf","transparent",223,1160,"#mainflash");
	});
});
