#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133

from django.contrib import admin
# Register your models here.
from app.models import Recipe, Ingredient, Instruction, Task, IngredientItem, Module, StockGroup, Coordinates, Setting

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientItem)
admin.site.register(Module)
admin.site.register(Instruction)
admin.site.register(Task)
admin.site.register(StockGroup)
admin.site.register(Coordinates)
admin.site.register(Setting)
