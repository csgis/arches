define(['arches',
    'models/abstract',
    'models/card',
    'knockout',
    'knockout-mapping',
    'underscore'
], function (arches, AbstractModel, CardModel, ko, koMapping, _) {
    var ReportModel = AbstractModel.extend({
        /**
        * A backbone model to manage report data
        * @augments AbstractModel
        * @constructor
        * @name ReportModel
        */

        url: arches.urls.report_editor,

        initialize: function(options){
            var self = this;

            options.forms.forEach(function (form) {
                form.cards = [];
                options.forms_x_cards.forEach(function (form_x_card) {
                    if (form_x_card.form_id === form.formid) {
                        var card = _.find(options.cards, function (card) {
                            return card.cardid === form_x_card.card_id;
                        });
                        var cardModel = new CardModel({
                            data: card,
                            datatypes: options.datatypes
                        });
                        cardModel.formId = form.formid;
                        form.cards.push(cardModel);
                    }
                })
                form.sortorder = Infinity;
            });
            this.forms = ko.observableArray(options.forms);

            this.set('reportid', ko.observable());
            this.set('name', ko.observable());
            this.set('template_id', ko.observable());
            this.set('graph', ko.observable());
            this.set('active', ko.observable());
            this.set('config', {});
            self.configKeys = ko.observableArray();

            this._data = ko.observable('{}');

            this.dirty = ko.computed(function(){
                return JSON.stringify(_.extend(JSON.parse(self._data()),self.toJSON())) !== self._data();
            });

            this.parse(options.report);
        },

        /**
         * parse - parses the passed in attributes into a {@link ReportModel}
         * @memberof ReportModel.prototype
         * @param  {object} attributes - the properties to seed a {@link ReportModel} with
         */
        parse: function(attributes){
            var self = this;
            this._attributes = attributes;

            _.each(attributes, function(value, key){
                switch(key) {
                    case 'reportid':
                        this.set('id', value);
                    case 'name':
                    case 'template_id':
                    case 'graph':
                    case 'active':
                        this.get(key)(value);
                        break;
                    case 'config':
                        var config = {};
                        self.configKeys.removeAll();
                        _.each(value, function(configVal, configKey) {
                            config[configKey] = ko.observable(configVal);
                            self.configKeys.push(configKey);
                        });
                        this.set(key, config);
                        break;
                    case 'formsconfig':
                        var forms = self.forms();
                        _.each(value, function(formconfig, formid) {
                            var form = _.find(forms, function(form) {
                                return form.formid === formid;
                            });
                            form.sortorder = formconfig.sortorder;
                        });
                    default:
                        this.set(key, value);
                }
            }, this);

            this.forms.sort(function (f1, f2) {
                return f1.sortorder > f2.sortorder;
            });

            this._data(JSON.stringify(this.toJSON()));
        },

        reset: function () {
            this._attributes  = JSON.parse(this._data());
            this.parse(this._attributes);
        },

        toJSON: function(){
            var ret = {};
            for(var key in this.attributes){
                if (ko.isObservable(this.attributes[key])){
                    ret[key] = this.attributes[key]();
                } else if (key === 'config') {
                    var configKeys = this.configKeys();
                    var config = null;
                    if (configKeys.length > 0) {
                        config = {};
                        _.each(configKeys, function(configKey) {
                            config[configKey] = self.config[configKey]();
                        });
                    }
                    ret[key] = config;
                } else {
                    ret[key] = this.attributes[key];
                }
            }
            ret.formsconfig = {};
            this.forms().forEach(function(form, i) {
                ret.formsconfig[form.formid] = {
                    sortorder: i
                };
            });
            return ret;
        },

        save: function(){
            AbstractModel.prototype.save.call(this, function(request, status, self){
                if(status === 'success'){
                    this._data(JSON.stringify(this.toJSON()));
                }
            }, this);
        }
    });
    return ReportModel;
});
