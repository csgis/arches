'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from django.views.decorators.cache import cache_page
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from arches.app.views import concept, main, map, search, graph, tileserver, api
from arches.app.views.admin import ReIndexResources
from arches.app.views.graph import GraphDesignerView, GraphManagerView, GraphSettingsView, NewGraphSettingsView, GraphDataView, DatatypeTemplateView, CardManagerView, CardView, FormManagerView, FormView, ReportManagerView, ReportEditorView, FunctionManagerView, PermissionManagerView, PermissionDataView
from arches.app.views.resource import ResourceEditorView, ResourceListView, ResourceData, ResourceCards, ResourceReportView, ResourceReportData, RelatedResourcesView, ResourceDescriptors, ResourceEditLogView, ResourceTiles
from arches.app.views.resource import NewResourceEditorView
from arches.app.views.concept import RDMView
from arches.app.views.user import UserManagerView
from arches.app.views.tile import TileData
from arches.app.views.map import MapLayerManagerView
from arches.app.views.mobile_survey import MobileSurveyManagerView, MobileSurveyResources
from arches.app.views.auth import LoginView, SignupView, ConfirmSignupView, ChangePasswordView, GetTokenView
from arches.app.models.system_settings import settings
from arches.app.utils.forms import ArchesPasswordResetForm
from arches.app.utils.forms import ArchesSetPasswordForm
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

uuid_regex = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'

urlpatterns = [
    url(r'^$', main.index, name='root'),
    url(r'^index.htm', main.index, name='home'),
    url(r'^auth/password$', ChangePasswordView.as_view(), name='change_password'),
    url(r'^auth/signup$', SignupView.as_view(), name='signup'),
    url(r'^auth/confirm_signup$', ConfirmSignupView.as_view(), name='confirm_signup'),
    url(r'^auth/get_token$', GetTokenView.as_view(), name='get_token'),
    url(r'^auth/', LoginView.as_view(), name='auth'),
    url(r'^rdm/(?P<conceptid>%s|())$' % uuid_regex , RDMView.as_view(), name='rdm'),
    url(r'^admin/reindex/resources$', ReIndexResources.as_view(), name="reindex"),
    url(r'^concepts/(?P<conceptid>%s)/manage_parents/$' % uuid_regex, concept.manage_parents, name="concept_manage_parents"),
    url(r'^concepts/(?P<conceptid>%s)/confirm_delete/$' % uuid_regex, concept.confirm_delete, name="confirm_delete"),
    url(r'^concepts/(?P<conceptid>%s)/make_collection/$' % uuid_regex, concept.make_collection, name="make_collection"),
    url(r'^concepts/(?P<conceptid>%s|())$' % uuid_regex , concept.concept, name="concept"),
    url(r'^concepts/tree/(?P<mode>.*)', concept.concept_tree, name="concept_tree"),
    url(r'^concepts/search$', concept.search, name="concept_search"),
    url(r'^concepts/(?P<conceptid>%s)/from_sparql_endpoint$' % uuid_regex, concept.add_concepts_from_sparql_endpoint, name="from_sparql_endpoint"),
    url(r'^concepts/search_sparql_endpoint$', concept.search_sparql_endpoint_for_concepts, name="search_sparql_endpoint"),
    url(r'^concepts/dropdown', concept.dropdown, name="dropdown"),
    url(r'^concepts/paged_dropdown', concept.paged_dropdown, name="paged_dropdown"),
    url(r'^concepts/export/(?P<conceptid>%s)$' % uuid_regex , concept.export, name="export_concept"),
    url(r'^concepts/export/collections', concept.export_collections, name="export_concept_collections"),
    url(r'^concepts/collections', concept.get_concept_collections, name="get_concept_collections"),
    url(r'^concepts/get_pref_label', concept.get_pref_label, name="get_pref_label"),
    url(r'^conceptvalue/', concept.concept_value, name="concept_value"),
    url(r'^search$', search.SearchView.as_view(), name="search_home"),
    url(r'^search/terms$', search.search_terms, name="search_terms"),
    url(r'^search/resources$', search.search_results, name="search_results"),
    url(r'^search/export$', search.export_results, name="search_results_export"),
    url(r'^search/time_wheel_config$', search.time_wheel_config, name="time_wheel_config"),
    url(r'^buffer/$', search.buffer, name="buffer"),
    url(r'^settings/', ResourceEditorView.as_view(), { 'resourceid': settings.RESOURCE_INSTANCE_ID, 'view_template':'views/system-settings.htm', 'main_script':'views/system-settings', 'nav_menu':False}, name='config'),
    url(r'^graph/new$', GraphDataView.as_view(action='new_graph'), name='new_graph'),
    url(r'^graph/import/', GraphDataView.as_view(action='import_graph'), name='import_graph'),
    url(r'^graph/permissions$', PermissionDataView.as_view(), name='permission_data'),
    url(r'^graph/(?P<graphid>%s|())$' % uuid_regex, GraphManagerView.as_view(), name='graph'),
    url(r'^graph/(?P<graphid>%s)/settings$' % uuid_regex, GraphSettingsView.as_view(), name='graph_settings'),
    url(r'^graph/(?P<graphid>%s)/card_manager$' % uuid_regex, CardManagerView.as_view(), name='card_manager'),
    url(r'^graph/(?P<graphid>%s)/append_branch$' % uuid_regex, GraphDataView.as_view(action='append_branch'), name='append_branch'),
    url(r'^graph/(?P<graphid>%s)/append_node$' % uuid_regex, GraphDataView.as_view(action='append_node'), name='append_node'),
    url(r'^graph/(?P<graphid>%s)/move_node$' % uuid_regex, GraphDataView.as_view(action='move_node'), name='move_node'),
    url(r'^graph/(?P<graphid>%s)/update_node$' % uuid_regex, GraphDataView.as_view(action='update_node'), name='update_node'),
    url(r'^graph/(?P<graphid>%s)/delete_node$' % uuid_regex, GraphDataView.as_view(action='delete_node'), name='delete_node'),
    url(r'^graph/(?P<graphid>%s)/clone$' % uuid_regex, GraphDataView.as_view(action='clone_graph'), name='clone_graph'),
    url(r'^graph/(?P<graphid>%s)/export$' % uuid_regex, GraphDataView.as_view(action='export_graph'), name='export_graph'),
    url(r'^graph/(?P<graphid>%s)/export_mapping_file$' % uuid_regex, GraphDataView.as_view(action='export_mapping_file'), name='export_mapping_file'),
    url(r'^graph/(?P<graphid>%s)/get_related_nodes/(?P<nodeid>%s)$' % (uuid_regex, uuid_regex), GraphDataView.as_view(action='get_related_nodes'), name='get_related_nodes'),
    url(r'^graph/(?P<graphid>%s)/get_valid_domain_nodes/(?P<nodeid>%s|())$' % (uuid_regex, uuid_regex), GraphDataView.as_view(action='get_valid_domain_nodes'), name='get_valid_domain_nodes'),
    url(r'^graph/(?P<graphid>%s)/get_domain_connections$' % uuid_regex, GraphDataView.as_view(action='get_domain_connections'), name='get_domain_connections'),
    url(r'^graph/(?P<graphid>%s)/form_manager$' % uuid_regex, FormManagerView.as_view(), name='form_manager'),
    url(r'^graph/(?P<graphid>%s)/add_form$' % uuid_regex, FormManagerView.as_view(action='add_form'), name='add_form'),
    url(r'^graph/(?P<graphid>%s)/reorder_forms$' % uuid_regex, FormManagerView.as_view(action='reorder_forms'), name='reorder_forms'),
    url(r'^graph/(?P<graphid>%s)/report_manager$' % uuid_regex, ReportManagerView.as_view(), name='report_manager'),
    url(r'^graph/(?P<graphid>%s)/add_report$' % uuid_regex, ReportManagerView.as_view(), name='add_report'),
    url(r'^graph/(?P<graphid>%s)/function_manager$' % uuid_regex, FunctionManagerView.as_view(), name='function_manager'),
    url(r'^graph/(?P<graphid>%s)/apply_functions$' % uuid_regex, FunctionManagerView.as_view(), name='apply_functions'),
    url(r'^graph/(?P<graphid>%s)/remove_functions$' % uuid_regex, FunctionManagerView.as_view(), name='remove_functions'),
    url(r'^graph/(?P<graphid>%s)/permissions$' % uuid_regex, PermissionManagerView.as_view(), name='permission_manager'),
    url(r'^graph_designer/(?P<graphid>%s)$' % uuid_regex, GraphDesignerView.as_view(), name='graph_designer'),
    url(r'^graph_settings/(?P<graphid>%s)$' % uuid_regex, NewGraphSettingsView.as_view(), name='new_graph_settings'),
    url(r'^components/datatypes/(?P<template>[a-zA-Z_-]*)', DatatypeTemplateView.as_view(), name='datatype_template'),
    url(r'^resource$', ResourceListView.as_view(), name='resource'),
    url(r'^resource/(?P<resourceid>%s)/(?P<graphid>%s)/add_resource$' % (uuid_regex, uuid_regex), ResourceEditorView.as_view(), name='add_resource'),
    url(r'^resource/(?P<resourceid>%s)$' % uuid_regex, ResourceEditorView.as_view(), name='resource_editor'),
    url(r'^resource-new/(?P<resourceid>%s)$' % uuid_regex, NewResourceEditorView.as_view(), name='new_resource_editor'),
    url(r'^add-resource/(?P<graphid>%s)$' % uuid_regex, NewResourceEditorView.as_view(), name='add_resource'),
    url(r'^resource/(?P<resourceid>%s)/copy$' % uuid_regex, ResourceEditorView.as_view(action='copy'), name='resource_copy'),
    url(r'^resource/(?P<resourceid>%s)/history$' % uuid_regex, ResourceEditLogView.as_view(), name='resource_edit_log'),
    url(r'^resource/(?P<resourceid>%s)/data/(?P<formid>%s)$' % (uuid_regex, uuid_regex), ResourceData.as_view(), name='resource_data'),
    url(r'^resource/(?P<resourceid>%s)/cards$' % uuid_regex, ResourceCards.as_view(), name='resource_cards'),
    url(r'^resource/history$', ResourceEditLogView.as_view(), name="edit_history"),
    url(r'^resource/related/(?P<resourceid>%s|())$' % uuid_regex, RelatedResourcesView.as_view(), name="related_resources"),
    url(r'^resource/descriptors/(?P<resourceid>%s|())$' % uuid_regex, ResourceDescriptors.as_view(), name="resource_descriptors"),
    url(r'^resource/(?P<resourceid>%s)/tiles$' % uuid_regex, ResourceTiles.as_view(), name='resource_tiles'),
    url(r'^report/(?P<resourceid>%s)$' % uuid_regex, ResourceReportView.as_view(), name='resource_report'),
    url(r'^report/(?P<resourceid>%s)$' % uuid_regex, ResourceReportView.as_view(), name='resource_report'),
    url(r'^card/(?P<cardid>%s|())$' % uuid_regex, CardView.as_view(), name='card'),
    url(r'^form/(?P<formid>%s|())$' % uuid_regex, FormView.as_view(), name='form'),
    url(r'^form/(?P<formid>%s)/delete$' % uuid_regex, FormView.as_view(), name='delete_form'),
    url(r'^report_editor/(?P<reportid>%s|())$' % uuid_regex, ReportEditorView.as_view(), name='report_editor'),
    url(r'^report/data$', ResourceReportData.as_view(), name='report_data'),
    url(r'^node/(?P<graphid>%s)$' % uuid_regex, GraphDataView.as_view(action='update_node'), name='node'),
    url(r'^node_layer/(?P<graphid>%s)$' % uuid_regex, GraphDataView.as_view(action='update_node_layer'), name='node_layer'),
    url(r'^widgets/(?P<template>[a-zA-Z_-]*)', main.widget, name="widgets"),
    url(r'^report-templates/(?P<template>[a-zA-Z_-]*)', main.report_templates, name="report-templates"),
    url(r'^function-templates/(?P<template>[a-zA-Z_-]*)', main.function_templates, name="function-templates"),
    url(r'^help-templates$', main.help_templates, name="help_templates"),
    url(r'^tile$', TileData.as_view(action='update_tile'), name="tile"),
    url(r'^tiles/reorder_tiles$', TileData.as_view(action='reorder_tiles'), name='reorder_tiles'),
    url(r'^tiles/delete_provisional_tile$', TileData.as_view(action='delete_provisional_tile'), name='delete_provisional_tile'),
    url(r'^templates/(?P<template>[a-zA-Z_\-./]*)', main.templates, name="templates"),
    url(r'^tileserver/*', tileserver.handle_request, name="tileserver"),
    url(r'^map_layer_manager/(?P<maplayerid>%s)$' % uuid_regex, MapLayerManagerView.as_view(), name='map_layer_update'),
    url(r'^map_layer_manager/*', MapLayerManagerView.as_view(), name="map_layer_manager"),
    url(r'^feature_popup_content$', main.feature_popup_content, name="feature_popup_content"),
    url(r'^user$', UserManagerView.as_view(), name="user_profile_manager"),
    url(r'^user/get_user_names$', UserManagerView.as_view(action='get_user_names'), name="get_user_names"),
    url(r'^mobile_survey_resources/(?P<surveyid>%s)/resources$' % uuid_regex, MobileSurveyResources.as_view(), name='mobile_survey_resources'),
    url(r'^mobile_survey_manager/*', MobileSurveyManagerView.as_view(), name="mobile_survey_manager"),
    url(r'^couchdb/(?P<path>.*)$', api.CouchdbProxy.as_view()),
    url(r'^surveys$', api.Surveys.as_view(), name='surveys'),
    url(r'^resources/(?P<resourceid>%s|())$' % uuid_regex, api.Resources.as_view(), name='surveys'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset', kwargs={"password_reset_form":ArchesPasswordResetForm}),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm', kwargs={"set_password_form":ArchesSetPasswordForm}),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2')),
]


if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except:
        pass
