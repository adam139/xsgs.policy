require([
  'jquery','jqswfobj','bootstrap-carousel'
], function($,jqswf,carousel) {
  'use strict';
$(document).ready(function(){
//		rolltext(".roll-wrapper");
	var w1=$('#mainflash').width();
		genswf("http://images.315ok.org/xsgs998/main.swf","transparent",223,w1,"#mainflash");
	});
});
