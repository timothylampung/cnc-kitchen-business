#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


from django.conf.urls import url
from app.api.views import IngredientDetailAPIView, IngredientAPIView, ModuleAPIView, ModuleDetailAPIView, RecipeAPIView, \
    RecipeDetailAPIView, InstructionAPIView, InstructionDetailAPIView, StockGroupAPIView, StockGroupDetailAPIView, \
    TaskAPIView, TaskDetailAPIView, IngredientItemsAPIView, IngredientItemsDetailAPIView, CoordinatesAPIView, \
    CoordinatesDetailAPIView, SettingsAPIView, SettingsDetailAPIView, CookStateAPIView, CookStateDetailAPIView
from stir_fry.api.views import TaskExecutionView

urlpatterns = [
    url(r'^stock-groups/$', StockGroupAPIView.as_view(), name='create_or_find_all_stock_group'),
    url(r'^stock-groups/(?P<pk>\d+)/$', StockGroupDetailAPIView.as_view(),
        name='update_or_delete_or_find_stock_group_by_id'),
    url(r'^stock-groups/(?P<group>\d+)/ingredients/$', IngredientAPIView.as_view(),
        name='create_or_find_all_ingredient'),
    url(r'^ingredients/$', IngredientAPIView.as_view(), name='create_or_find_all_ingredient'),
    url(r'^ingredients/(?P<pk>\d+)/$', IngredientDetailAPIView.as_view(),
        name='update_or_delete_or_find_ingredient_by_id'),
    url(r'^modules/$', ModuleAPIView.as_view(), name='create_or_find_all_module'),
    url(r'^modules/(?P<pk>\d+)/$', ModuleDetailAPIView.as_view(), name='update_or_delete_or_find_module_by_id'),
    url(r'^recipes/$', RecipeAPIView.as_view(), name='create_or_find_all_recipe'),
    url(r'^recipes/(?P<pk>\d+)/$', RecipeDetailAPIView.as_view(), name='update_or_delete_or_find_recipe_by_id'),
    url(r'^recipes/(?P<recipe>\d+)/instructions/$', InstructionAPIView.as_view(),
        name='find_all_categories_by_business_id'),
    url(r'^instructions/(?P<pk>\d+)/$', InstructionDetailAPIView.as_view(),
        name='update_or_delete_or_find_recipe_by_id'),
    url(r'^tasks/$', TaskAPIView.as_view(), name='create_or_find_all_tasks'),
    url(r'^tasks-by-modules/$', TaskExecutionView.as_view(), name='find_all_tasks_by_module'),
    url(r'^tasks/(?P<pk>\d+)/$', TaskDetailAPIView.as_view(), name='update_or_delete_or_find_task_by_id'),
    url(r'^(?P<instruction>\d+)/ingredient-items/$', IngredientItemsAPIView.as_view(), name='create_or_find_all_tasks'),
    url(r'^ingredient-items/(?P<pk>\d+)/$', IngredientItemsDetailAPIView.as_view(),
        name='update_or_delete_or_find_task_by_id'),
    url(r'^coordinates/$', CoordinatesAPIView.as_view(), name='create_or_find_all_tasks'),
    url(r'^coordinates/(?P<pk>\d+)/$', CoordinatesDetailAPIView.as_view(), name='update_or_delete_or_find_task_by_id'),

    url(r'^settings/$', SettingsAPIView.as_view(), name='create settings'),
    url(r'^settings/(?P<pk>\d+)/$', SettingsDetailAPIView.as_view(), name='update_or_delete_or_find_settings_by_id'),

    url(r'^cook-states/$', CookStateAPIView.as_view(), name='create_cook_state'),
    url(r'^cook-states/(?P<pk>\d+)/$', CookStateDetailAPIView.as_view(),
        name='update_or_delete_or_find_CookState_by_id'),
]
