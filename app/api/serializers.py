#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


from app.models import Module, Recipe, Ingredient, Instruction, IngredientItem, Task, StockGroup, Coordinates, \
    CookState, Setting
from app.serializers import DocumentModelSerializer
from rest_framework import serializers


class ModuleSerializer(DocumentModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class CoordinateSerializer(DocumentModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'


class IngredientSerializer(DocumentModelSerializer):
    # image_path = serializers.ImageField(allow_null=True, allow_empty_file=True)
    coordinate = CoordinateSerializer(source='coordinate_id', many=False, read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def save(self, **kwargs):
        return super().save()


class StockGroupSerializer(DocumentModelSerializer):
    class Meta:
        model = StockGroup
        fields = '__all__'


class IngredientSummarySerializer(DocumentModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientItemSerializer(DocumentModelSerializer):
    ingredient_name = serializers.StringRelatedField(source="ingredient_id", read_only=True)
    ingredient = IngredientSummarySerializer(source='ingredient_id', many=False, read_only=True)

    class Meta:
        model = IngredientItem
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class InstructionSerializer(DocumentModelSerializer):
    ingredient_items_of_instruction = IngredientItemSerializer(many=True, read_only=True)

    class Meta:
        model = Instruction
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class CookStateSerializer(DocumentModelSerializer):
    class Meta:
        model = CookState
        fields = '__all__'

    def validate(self, attrs):
        return attrs


class RecipeSerializer(DocumentModelSerializer):
    instructions_of_recipe = InstructionSerializer(many=True, read_only=True)
    cook_states_of_recipe = CookStateSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeSummarySerializer(DocumentModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        # exclude = ('rating',)


class SettingsSerializer(DocumentModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'
        # exclude = ('rating',)


class TaskSerializer(DocumentModelSerializer):
    recipe = RecipeSummarySerializer(source='recipe_id', read_only=True, many=False)
    module = ModuleSerializer(source='module_id', read_only=True, many=False)

    class Meta:
        model = Task
        fields = '__all__'


class TaskViewSerializer(DocumentModelSerializer):
    tasks_run_on_module = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'
