$(function(){

	var BASE_URL = "http://localhost:5000";
	var API_URL = "/api/v1/feature/"
	function getUrl(url) {
		return BASE_URL.concat(url);
	}

	var currentDate = (new Date()).toISOString().split('T')[0];

	function Feature(data){
		this.id = data.id;
		this.title = data.title;
		this.description = ko.observable(data.description);
		this.target_date = ko.observable(data.target_date);
		this.priority = ko.observable(data.priority);
	}

	function FeatureListViewModel(){
		//data
		var self = this;

		self.features = ko.observableArray([]);

		self.newFeatureTitle = ko.observable();
		self.newFeatureDescription = ko.observable();
		self.newFeaturePriority = ko.observable();

		self.selectedFeatureData = ko.observable();
		self.shouldEditData = ko.observable();
		self.shouldCreateData = ko.observable();

		self.inputdate = ko.observable(currentDate);

		//routing functions
		self.goToFeatureList = function() { location.hash = '' };

		self.goToFeature = function(feature) { 
			location.hash ='/feature/' +feature.id 
		};
		self.editFeature = function(feature) { 
			location.hash = '/edit/' +feature.id 
		};
		self.goToCreateFeature = function(){
			window.location = BASE_URL + '#create';
		}

		//callback functions
		self.getFeatureCallBack = function(featureData){
			var mappedFeature = new Feature(featureData);
			self.selectedFeatureData(mappedFeature);
			self.shouldEditData(false);
			self.shouldCreateData(false);
		};
		self.getFeatureToEditCallBack = function(featureData){
			var mappedFeature = new Feature(featureData);
			self.selectedFeatureData(mappedFeature);
			self.shouldEditData(true);
			self.shouldCreateData(false);
		};
		self.getFeatureListCallBack = function(featureList){
			var mappedFeatures = $.map(featureList[0], function(feature) { return new Feature(feature)});
			self.features(mappedFeatures);
			self.selectedFeatureData(null);
			self.shouldEditData(false);
			self.shouldCreateData(false);
		}
		self.createFeatureCallBack = function(){

			self.selectedFeatureData(null);
			self.shouldEditData(false);
			self.shouldCreateData(true);

		}

		//helper
		function restCreateMethod(){
			self.newFeatureTitle(null);
			self.newFeatureDescription(null);
			self.newFeaturePriority(null);
		}

		//ajax methods
		self.create = function() {

			newFeature = new Feature({
				title:self.newFeatureTitle,
				description:self.newFeatureDescription, 
				priority:self.newFeaturePriority,
				target_date:self.inputdate
			})
			console.log(newFeature);
			var url = getUrl("/api/v1/feature")

	        $.ajax(url, {
	            data: ko.toJSON(newFeature),
	            type: "POST", contentType: "application/json",
	            success: function(result) { 
	            	console.log(result);
	            	self.goToFeatureList();
	            }
	        });
		};


		self.update = function() {
			var url = getUrl("/api/v1/feature/") + self.selectedFeatureData().id;
	        $.ajax(url, {
	            data: ko.toJSON(self.selectedFeatureData),
	            type: "PUT", contentType: "application/json",
	            success: function(result) { 
	            	console.log(result);
	            	self.goToFeatureList();
	            }
	        });
		};

		self.deleteFeature = function(){
			var url = getUrl("/api/v1/feature/") + self.selectedFeatureData().id;
			$.ajax(url, {
	            data: ko.toJSON(self.selectedFeatureData),
	            type: "Delete", contentType: "application/json",
	            success: function(result) { 
	            	console.log(result);
	            	self.goToFeatureList();
	            }
	        });
		}


	    Sammy(function() {

	    	//default
		    this.get('#/index', function() {
		        var url = getUrl("/api/v1/feature");
		        $.getJSON(url,self.getFeatureListCallBack);     
			});

			this.get('#/feature/:id', function() {
				var url = getUrl("/api/v1/feature/") + this.params.id;
		        $.getJSON(url,self.getFeatureCallBack);        
			});
			
			this.get('#/edit/:id', function() {
		        var url = getUrl("/api/v1/feature/") + this.params.id;
				$.getJSON(url,self.getFeatureToEditCallBack);        
			});
			this.get('#create', function() {
				self.createFeatureCallBack();
			});

	    	this.get('', function() { this.app.runRoute('get', '#/index') });

	    }).run();
	}
	ko.applyBindings(new FeatureListViewModel());

});