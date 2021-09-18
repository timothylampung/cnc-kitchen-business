#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


import threading
import os
from rest_framework import mixins, generics, pagination
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.api.serializers import IngredientSerializer, ModuleSerializer, RecipeSerializer, InstructionSerializer, \
    StockGroupSerializer, TaskSerializer, IngredientItemSerializer, CoordinateSerializer, TaskViewSerializer, \
    SettingsSerializer, CookStateSerializer
from app.models import Ingredient, Module, Recipe, Instruction, StockGroup, Task, IngredientItem, Coordinates, Setting, \
    CookState


class CustomPaginationClass(pagination.PageNumberPagination):
    page_size = 50


@permission_classes((AllowAny,))
class ModuleAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Module.objects.all().order_by('timestamp')
    serializer_class = ModuleSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        qs = Module.objects.all().order_by('timestamp')
        query = self.request.GET.get('query')
        module_type = self.request.GET.get('type')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        if module_type is not None:
            qs = qs.filter(type=module_type)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class ModuleDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class IngredientAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Ingredient.objects.all().order_by('timestamp')
    serializer_class = IngredientSerializer
    pagination_class = CustomPaginationClass
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        qs = Ingredient.objects.all().order_by('timestamp')
        query = self.request.GET.get('query')
        g = None
        try:
            g = self.kwargs['group']
        except Exception as e:
            pass

        if g is not None:
            qs = qs.filter(group_id=g)
        if query is not None:
            qs = qs.filter(ingredient_name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class IngredientDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class StockGroupAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = StockGroup.objects.all().order_by('timestamp')
    serializer_class = StockGroupSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        qs = StockGroup.objects.all().order_by('timestamp')
        query = self.request.GET.get('query')
        if query is not None:
            qs = qs.filter(group_name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class StockGroupDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = StockGroup.objects.all()
    serializer_class = StockGroupSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroyg(request, *args, **kwargs)


@permission_classes((AllowAny,))
class RecipeAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Recipe.objects.all().order_by('timestamp')
    serializer_class = RecipeSerializer
    pagination_class = CustomPaginationClass
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        qs = Recipe.objects.all().order_by('timestamp')
        query = self.request.GET.get('query')
        if query is not None:
            qs = qs.filter(recipe_name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class RecipeDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class InstructionAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        try:
            recipe = self.kwargs['recipe']
            qs = Instruction.objects.all()
            query = self.request.GET.get('query')
            if recipe is not None:
                qs = qs.filter(recipe=recipe)
            if query is not None:
                qs = qs.filter(name__icontains=query)
            return qs
        except Exception as e:
            pass

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class InstructionDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Instruction.objects.all()
    serializer_class = InstructionSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class TaskAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        qs = Task.objects.all()
        query = self.request.GET.get('query')
        if query is not None and query != '':
            qs = qs.filter(task_name__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        try:
            module_id = request.data['module_id']
        except KeyError:
            module = Module.objects.filter(status=Module.AVAILABLE)[0]
            request.data['module_id'] = module.id
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class TaskDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class IngredientItemsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        try:
            instruction = self.kwargs['instruction']
            qs = IngredientItem.objects.all()
            query = self.request.GET.get('query')
            qs = qs.filter(instruction=instruction)
            if query is not None:
                qs = qs.filter(ingredient_ingredient_name__icontains=query)
            return qs
        except Exception as e:
            pass

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class IngredientItemsDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = IngredientItem.objects.all()
    serializer_class = IngredientItemSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class CoordinatesAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Coordinates.objects.all()
    serializer_class = CoordinateSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        try:
            qs = Coordinates.objects.all()
            query = self.request.GET.get('query')
            if query is not None:
                qs = qs.filter(name__icontains=query)
            return qs
        except Exception as e:
            pass

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class CoordinatesDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Coordinates.objects.all()
    serializer_class = CoordinateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class SettingsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingsSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        try:
            qs = Setting.objects.all()
            query = self.request.GET.get('query')
            if query is not None:
                qs = qs.filter(name__icontains=query)
            return qs
        except Exception as e:
            pass

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class SettingsDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingsSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@permission_classes((AllowAny,))
class CookStateAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = CookState.objects.all()
    serializer_class = CookStateSerializer
    pagination_class = CustomPaginationClass

    def get_queryset(self):
        qs = CookState.objects.all()
        try:
            query = self.request.GET.get('query')
            if query is not None:
                qs = qs.filter(state_label__icontains=query)
        except Exception as e:
            pass
        try:
            recipe_id = self.request.GET.get('recipe_id')
            if recipe_id is not None:
                if isinstance(recipe_id, int):
                    recipe = Recipe.objects.get(pk=recipe_id)
                    qs = qs.filter(recipe_id=recipe)
        except Exception as e:
            pass

        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@permission_classes((AllowAny,))
class CookStateDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = CookState.objects.all()
    serializer_class = CookStateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
