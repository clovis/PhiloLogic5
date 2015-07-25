philoApp.directive('sidebarMenu', ['$rootScope', function($rootScope) {
    var populateFacets = function() {
        var facets = [];
        for (var i=0; i < $rootScope.philoConfig.facets.length; i++) {
            var alias = Object.keys($rootScope.philoConfig.facets[i])[0];
            var facet = $rootScope.philoConfig.facets[i][alias];
            if (typeof(facet) === "object") {
                facet = JSON.stringify(facet);
            }
            facets.push({facet: facet, alias: alias, type: 'facet'});
        }
        return facets;
    }
    var populateCollocationFacets = function() {
        var collocationFacets = [
            {facet: "all_collocates",  alias: "in the same sentence", type: "collocationFacet"},
        ];
        return collocationFacets;
    }
    var populateWordFacets = function() {
        var wordsFacets = [];
        for (var i=0; i < $rootScope.philoConfig.words_facets.length; i++) {
            var alias = Object.keys($rootScope.philoConfig.words_facets[i])[0];
            var facet = $rootScope.philoConfig.words_facets[i][alias];
            wordsFacets.push({facet: facet, alias: alias, type: 'wordFacet'});
        }
        return wordsFacets;
    }
    return {
        restrict: 'E',
        templateUrl: 'app/components/concordanceKwic/sidebarMenu.html',
		replace: true,
        link: function(scope) {
            scope.facets = populateFacets();
            scope.collocationFacets = populateCollocationFacets();
            scope.wordsFacets = populateWordFacets();
        }
    }
}]);

philoApp.directive('facets', ['$rootScope', '$location', '$http', 'URL', 'progressiveLoad', 'saveToLocalStorage', 'request', function($rootScope, $location, $http, URL, progressiveLoad, save, request) {
    var retrieveFacet = function(scope, facetObj) {
		scope.facet = facetObj;
        var urlString = $location.url() + '&frequency_field=' + facetObj.alias;
        if (typeof(sessionStorage[urlString]) !== "undefined" && $rootScope.philoConfig.production === true) {
			scope.loading = true;
			scope.fullResults = JSON.parse(sessionStorage[urlString]);
			scope.concKwic.frequencyResults = scope.fullResults.sorted.slice(0,500);
			scope.loading = false;
            scope.percent = 100;
        } else {
            // store the selected field to check whether to kill the ajax calls in populate_sidebar
            $('#selected-sidebar-option').data('selected', facetObj.alias);
            $('#selected-sidebar-option').data('interrupt', false);
			scope.done = false;
            var fullResults = {};
            scope.loading = true;
            scope.moreResults = true;
            scope.percent = 0;
            var queryParams = angular.copy($rootScope.formData);
            if (facetObj.type === "facet") {
                queryParams.script = "get_frequency.py";
                queryParams.frequency_field = JSON.stringify(facetObj.facet);
            } else if (facetObj.type === "collocationFacet") {
                queryParams.report = "collocation";
            } else {
                queryParams.field = facetObj.facet;
                queryParams.script = "get_word_frequency.py";
            }
            populateSidebar(scope, facetObj, fullResults, 0, 3000, queryParams);
        }
    }
    var populateSidebar = function(scope, facet, fullResults, start, end, queryParams) {
		if (scope.moreResults) {
			if (facet.type !== "collocationFacet") {
				var promise = request.script(queryParams, {start: start, end: end});
			} else {
				var promise = request.report(queryParams, {start: start});
			}
			promise.then(function(response) {
				var results = response.data.results;
				scope.moreResults = response.data.more_results;
				scope.resultsLength = response.data.results_length;
				scope.sidebarHeight = {height: $('#results_container').height() - 40 + 'px'};
				if ($('#selected-sidebar-option').data('interrupt') != true && $('#selected-sidebar-option').data('selected') == facet.alias) {
					if (facet.type === "collocationFacet") {
						var merge = progressiveLoad.mergeResults(fullResults.unsorted, response.data.collocates);
						end = response.data.hits_done
					} else {
						var merge = progressiveLoad.mergeResults(fullResults.unsorted, results);
					}
					scope.concKwic.frequencyResults = merge.sorted.slice(0,500);
					scope.loading = false;
					fullResults = merge;
					if (end < scope.resultsLength) {
						$rootScope.percentComplete = end / scope.resultsLength * 100;
						scope.percent = Math.floor($rootScope.percentComplete);
					}
					if (facet.type === "collocationFacet") {
                        start = response.data.hits_done;
                    } else {
						if (start === 0) {
							start = 3000;
							end = 13000;
						} else {
							start += 10000;
							end += 10000;
						}
					}
					populateSidebar(scope, facet, fullResults, start, end, queryParams);
				} else {
					// This won't affect the full collocation report which can't be interrupted when on the page
					$('#selected-sidebar-option').data('interrupt', false);
				}
			}).catch(function(response) {
				scope.loading = false;
			});
		}  else {
			scope.percent = 100;
			scope.fullResults = fullResults;
			var urlString = $location.url() + '&frequency_field=' + scope.concKwic.selectedFacet.alias;
			save(fullResults, urlString);
		}
    }
	var getRelativeFrequencies = function(scope, hitsDone) {
		$http.post('scripts/get_metadata_token_count.py',
				   JSON.stringify({results: scope.fullResults.unsorted,	hits_done: hitsDone}))
		.then(function(response) {
			angular.merge(scope.fullRelativeFrequencies, response.data.frequencies);
			//scope.fullRelativeFrequencies = relativeResults.unsorted
			console.log(response.data.frequencies)
			var sortedRelativeResults = progressiveLoad.sortResults(scope.fullRelativeFrequencies);
			scope.concKwic.frequencyResults = angular.copy(sortedRelativeResults.slice(0, 500));
			scope.showingRelativeFrequencies = true;
			scope.loading = false;
			if (response.data.more_results) {
				console.log(sortedRelativeResults.length, scope.fullResults)
				scope.percent = Math.round(sortedRelativeResults.length / scope.fullResults.sorted.length * 100);
				getRelativeFrequencies(scope, response.data.hits_done)
			} else {
				scope.percent = 100
			}
		}).catch(function(response) {
			console.log(response);
			scope.loading = false;
		});	
	}
    return {
        restrict: 'E',
        templateUrl: 'app/components/concordanceKwic/facets.html',
		replace: true,
        link: function(scope, element, attrs) {
            attrs.$observe('facet', function(facetObj) {
                if (facetObj !== '') {
					scope.showingRelativeFrequencies = false;
					scope.relativeFrequencies = 'undefined';
                    facetObj = scope.$eval(facetObj);
                    retrieveFacet(scope, facetObj);
                }
            });
			scope.displayRelativeFrequencies = function() {
				scope.loading = true;
				if (scope.relativeFrequencies === 'undefined') {
					scope.absoluteFrequencies = angular.copy(scope.concKwic.frequencyResults);
					scope.percent = 0;
					scope.fullRelativeFrequencies = {};
					getRelativeFrequencies(scope, 0);
				} else {
					scope.absoluteFrequencies = angular.copy(scope.concKwic.frequencyResults);
					scope.concKwic.frequencyResults = scope.relativeFrequencies;
					scope.showingRelativeFrequencies = true;
					scope.loading = false;
				}
			}
			scope.displayAbsoluteFrequencies = function() {
				scope.loading = true;
				scope.relativeFrequencies = angular.copy(scope.concKwic.frequencyResults);
				scope.concKwic.frequencyResults = scope.absoluteFrequencies;
				scope.showingRelativeFrequencies = false;
				scope.loading = false;
			}
			scope.collocationToConcordance = function(word) {
				var q = $location.search().q + ' "' + word + '"';
				var newUrl = URL.objectToUrlString($location.search(),
												   {
													method: "cooc",
													start: "0",
													end: '0',
													q: q,
													report: "concordance"
												   });
				$location.url(newUrl);
			}
        }
    }
}]);