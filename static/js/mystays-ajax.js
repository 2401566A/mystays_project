$(document).ready(function() {
	$('#sort_by_overall_rating').click(function() {
		$.get('/mystays/WhereToStay/SortByRating/', function(data) {
			$('#sort_by_overall_rating').hide();
		})
	});

	$('#sort_by_price_value').click(function() {
		$.get('/mystays/WhereToStay/SortByPriceValue/', function(data) {
			$('#sort_by_price_value').hide();
		})
	});
});