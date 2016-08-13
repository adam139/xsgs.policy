require([
  'jquery'
], function($) {
  'use strict';
$(document).ready(function(){
	$("#mobile-entry").mouseover(function(){
		  $("#sn-qrcode").show();
		}); 
			$("#mobile-entry").mouseout(function(){
		  $("#sn-qrcode").hide();
		}); 
				$("#follow-entry").mouseover(function(){
		  $("#follow-qrcode").show();
		}); 
			$("#follow-entry").mouseout(function(){
		  $("#follow-qrcode").hide();
		});
});
});