define([
    'knockout',
    'underscore',
    'knockout-mapping',
    'uuid'
], function(ko, _, koMapping, uuid) {
    STEP_ID_LABEL = 'workflow-step-id';

    var WorkflowStep = function(config) {
        var self = this;

        this.id = ko.observable();
        this.workflowId = ko.observable(config.workflow ? config.workflow.id : null);

        this.classUnvisited = 'workflow-step-icon';
        this.classActive = 'workflow-step-icon active';
        this.classComplete = 'workflow-step-icon complete';
        this.classCanAdavance = 'workflow-step-icon can-advance';

        this.icon = 'fa-chevron-circle-right';
        this.title = '';
        this.subtitle = '';
        this.description = '';

        this.informationBoxData = ko.observable();        
        this.complete = ko.observable(false);
        this.required = ko.observable(ko.unwrap(config.required));
        this.autoAdvance = ko.observable(true);

        this.externalStepData = {};

        var externalStepSourceData = ko.unwrap(config.externalstepdata) || {};
        Object.keys(externalStepSourceData).forEach(function(key) {
            if (key !== '__ko_mapping__') {
                self.externalStepData[key] = {
                    stepName: externalStepSourceData[key],
                    data: config.workflow.getStepData(externalStepSourceData[key]),
                };
            }
        });
        delete config.externalstepdata;
        
        this.value = ko.observable();
        this.value.subscribe(function(value) {
            /* if we have defined that this is part of a single-resource workflow, and that this step creates the desired resource */ 
            if (self.shouldtrackresource && !ko.unwrap(config.workflow.resourceId)) {
                config.workflow.resourceId(value.resourceid)
            }
        });

        this.active = ko.computed(function() {
            return config.workflow.activeStep() === this;
        }, this);
        this.active.subscribe(function(active) {
            if (active) { 
                self.setStepIdToUrl(); 
                self.getExternalStepData();
            }
        });

        Object.keys(config).forEach(function(prop){
            if(prop !== 'workflow') {
                config[prop] = koMapping.fromJS(config[prop]);
            }
        });

        this.initialize = function() {
            /* cached ID logic */ 
            var cachedId = ko.unwrap(config.id);
            if (cachedId) {
                self.id(cachedId)
            }
            else {
                self.id(uuid.generate());
            }

            /* cached value logic */ 
            var cachedValue = self.getFromLocalStorage('value');
            if (cachedValue) {
                self.value(cachedValue);
                self.complete(true);
            }

            /* set value subscription */ 
            self.value.subscribe(function(value) {
                self.setToLocalStorage('value', value);
            });

            /* cached informationBox logic */ 
            if (config.informationboxdata) {
                self.informationBoxData({
                    hidden: self.getInformationBoxHiddenStateFromLocalStorage(),
                    heading: config.informationboxdata['heading'],
                    text: config.informationboxdata['text'],
                })
            }
        };

        this.setToLocalStorage = function(key, value) {
            localStorage.setItem(
                `${STEP_ID_LABEL}-${self.id()}`, 
                JSON.stringify({ [key]: value })
            );
        };

        this.getFromLocalStorage = function(key) {
            var localStorageData = JSON.parse(localStorage.getItem(`${STEP_ID_LABEL}-${self.id()}`));

            if (localStorageData) {
                return localStorageData[key];
            }
        };

        this.setStepIdToUrl = function() {
            var searchParams = new URLSearchParams(window.location.search);
            searchParams.set(STEP_ID_LABEL, self.id());

            var newRelativePathQuery = `${window.location.pathname}?${searchParams.toString()}`;
            history.pushState(null, '', newRelativePathQuery);
        };

        this.getExternalStepData = function() {
            Object.keys(self.externalStepData).forEach(function(key) {
                self.externalStepData[key]['data'] = config.workflow.getStepData(externalStepSourceData[key]);
            });
        }

        this.hideInformationBox = function() {
            var informationBoxData = self.informationBoxData();
            informationBoxData['hidden'] = true;

            self.informationBoxData(informationBoxData);
            self.setToLocalStorage('informationBoxHidden', true);
        };

        this.showInformationBox = function() {
            var informationBoxData = self.informationBoxData();
            informationBoxData['hidden'] = false;
            
            self.informationBoxData(informationBoxData);
            self.setToLocalStorage('informationBoxHidden', false);
        };

        this.getInformationBoxHiddenStateFromLocalStorage = function() {
            return self.getFromLocalStorage('informationBoxHidden')
        };

        _.extend(this, config);

        this.iconClass = ko.computed(function(){
            var ret = '';
            if(this.active()){
                ret = this.classActive;
            }else if(this.complete()){
                ret = this.classComplete;
            }else {
                ret = this.classUnvisited;
            }
            return ret + ' ' + ko.unwrap(this.icon);
        }, this);

        this.initialize();
    };
    
    /* only register template here, params are passed at the workflow level */ 
    ko.components.register('workflow-step', {
        template: {
            require: 'text!templates/views/components/plugins/workflow-step.htm'
        }
    });

    return WorkflowStep;
});
