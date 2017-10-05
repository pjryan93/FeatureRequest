$(function(){

	var BASE_URL = "";
	var API_URL = "/api/v1/feature/"
	function getUrl(url) {
		return BASE_URL.concat(url);
	}

	var currentDate = (new Date()).toISOString().split('T')[0];

	function reverseDate(date){
		return date.split('-').reverse().join('-');
	}

	function Feature(data){
		this.id = data.id;
		this.title = data.title;
		this.description = ko.observable(data.description);
		this.target_date = ko.observable(data.target_date);
		this.display_date = function(){
			console.log(data.target_date)
			return reverseDate(data.target_date.toString());
		};
		this.priority = ko.observable(data.priority);
	}

	function FeatureListViewModel(){
		//data
		var self = this;

		self.features = ko.observableArray([]);

		self.newFeatureTitle = ko.observable();
		self.newFeatureDescription = ko.observable();
		self.newFeaturePriority = ko.observable();
		self.inputdate = ko.observable(currentDate);

		self.selectedFeatureData = ko.observable(null);
		self.shouldEditData = ko.observable(false);
		self.shouldCreateData = ko.observable(false);


		self.maxPriority = ko.observable(null);

		//for createing a new feature the max priority needs to be 1 greater compated to when updating.
		self.maxPriorityForCreate = ko.computed(function(){
			console.log(self.maxPriority());
			return self.maxPriority() + 1;
		});

		//routing functions
		self.goToFeatureList = function() { location.hash = '' };

		self.goToFeature = function(feature) { 
			location.hash ='/feature/' +feature.id 
		};
		self.editFeature = function(feature) { 
			location.hash = '/edit/' +feature.id 
		};
		self.goToCreateFeature = function(){
			location.hash =  '#create';
		}

		//callback functions
		self.getFeatureCallBack = function(featureData){
			self.shouldEditData(false);
			self.shouldCreateData(false);
			var mappedFeature = new Feature(featureData);
			self.selectedFeatureData(mappedFeature);
		};

		self.getFeatureToEditCallBack = function(featureData){
			var mappedFeature = new Feature(featureData);
			self.shouldCreateData(false);
			self.shouldEditData(true);
			self.selectedFeatureData(mappedFeature);
		};

		self.getFeatureListCallBack = function(featureList){
			var mappedFeatures = $.map(featureList[0], function(feature) { return new Feature(feature)});
			self.selectedFeatureData(null);
			self.shouldEditData(false);
			self.shouldCreateData(false);
			self.features(mappedFeatures);
		}
		self.createFeatureCallBack = function(){

			self.selectedFeatureData(null);
			self.shouldEditData(false);
			self.shouldCreateData(true);

		}

		//helper
		function restCreateMethod() {
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
	            	self.newFeatureTitle(null);
	            	self.newFeaturePriority(null);
	            	self.inputdate(null);
	            	self.newFeatureDescription(null);
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

		self.getMaxPriority = function(callback){
			var url = getUrl("/api/v1/meta")
			$.ajax(url, {
	            type: "GET", contentType: "application/json",
	            success: function(result) { 
	            	self.maxPriority(result[0].feature_count)
	            	callback();
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
				self.getMaxPriority(function(){
					//very hacky need to fix 
					//when editing max priority should be one lower
					$.getJSON(url,self.getFeatureToEditCallBack)
				});        
			});

			this.get('#create', function() {
				self.getMaxPriority(self.createFeatureCallBack)
			});

	    	this.get('', function() { this.app.runRoute('get', '#/index') });

	    }).run();
	}
	ko.applyBindings(new FeatureListViewModel());

});