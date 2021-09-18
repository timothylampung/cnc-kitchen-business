#  Copyright (c) 2021.
#  Volume Research & Development sdn. bhd.
#  Author : Timothy Lampung
#  Email : timothylampung@gmail.com
#  Contacts : +601165315133


import uuid

from django.conf import settings
from django.db import models


# Create your models here.
class DocumentModel(models.Model):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

    DOCUMENT_STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )

    document_status = models.CharField(max_length=200, null=True, choices=DOCUMENT_STATUS_CHOICES, default=ACTIVE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name="%(class)s_editor",
                               )
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=True,
                                related_name="%(class)s_creator",
                                )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    document_code = models.CharField(null=True, blank=True, max_length=400)

    def save(self, **kwargs):
        if self.id is None:
            self.document_code = uuid.uuid4()
        super().save(**kwargs)

    class Meta:
        abstract = True


def upload_ingredient_image(instance, filename):
    return f"images/ingredients/{filename}"


def upload_recipe_image(instance, filename):
    return f"images/recipes/{filename}"


class Module(DocumentModel):
    STIR_FRY_MODULE = 'STIR_FRY_MODULE'
    DEEP_FRY_MODULE = 'DEEP_FRY_MODULE'
    GRILLING_MODULE = 'GRILLING_MODULE'
    DRINKS_MODULE = 'DRINKS_MODULE'
    BOILER_MODULE = 'BOILER_MODULE'
    STEAMING_MODULE = 'STEAMING_MODULE'
    TRANSPORTER_MODULE = 'TRANSPORTER_MODULE'

    TYPE = (
        (STIR_FRY_MODULE, 'STIR_FRY_MODULE'),
        (DEEP_FRY_MODULE, 'DEEP_FRY_MODULE'),
        (GRILLING_MODULE, 'GRILLING_MODULE'),
        (DRINKS_MODULE, 'DRINKS_MODULE'),
        (BOILER_MODULE, 'BOILER_MODULE'),
        (STEAMING_MODULE, 'STEAMING_MODULE'),
        (TRANSPORTER_MODULE, 'TRANSPORTER_MODULE'),
    )

    BUSY = 'BUSY'
    AVAILABLE = 'AVAILABLE'
    DISABLED = 'DISABLED'

    STATUS = (
        (BUSY, 'BUSY'),
        (AVAILABLE, 'AVAILABLE'),
        (DISABLED, 'DISABLED'),
    )

    BUSY = 'BUSY'
    AVAILABLE = 'AVAILABLE'
    DISABLED = 'DISABLED'

    CONNECTED = 'CONNECTED'
    DISCONNECTED = 'DISCONNECTED'

    CONNECTIVITY = (
        (CONNECTED, 'CONNECTED'),
        (DISCONNECTED, 'DISCONNECTED'),
    )

    name = models.CharField(null=True, blank=True, max_length=400)
    ip_address = models.CharField(null=True, blank=True, max_length=400)
    wok_camera = models.CharField(null=True, blank=True, max_length=400)
    camera_opened = models.BooleanField(default=False, null=True)
    port = models.IntegerField(default=8888)
    ui_port = models.IntegerField(default=8888)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default=AVAILABLE)
    connectivity = models.CharField(max_length=200, null=True, choices=CONNECTIVITY, default=DISCONNECTED)
    type = models.CharField(max_length=200, null=True, choices=TYPE, default=STIR_FRY_MODULE)


class Recipe(DocumentModel):
    STIR_FRY_MODULE = 'STIR_FRY_MODULE'
    DEEP_FRY_MODULE = 'DEEP_FRY_MODULE'
    GRILLING_MODULE = 'GRILLING_MODULE'
    DRINKS_MODULE = 'DRINKS_MODULE'
    BOILER_MODULE = 'BOILER_MODULE'
    STEAMING_MODULE = 'STEAMING_MODULE'
    TRANSPORTER_MODULE = 'TRANSPORTER_MODULE'

    TYPE = (
        (STIR_FRY_MODULE, 'STIR_FRY_MODULE'),
        (DEEP_FRY_MODULE, 'DEEP_FRY_MODULE'),
        (GRILLING_MODULE, 'GRILLING_MODULE'),
        (DRINKS_MODULE, 'DRINKS_MODULE'),
        (BOILER_MODULE, 'BOILER_MODULE'),
        (STEAMING_MODULE, 'STEAMING_MODULE'),
        (TRANSPORTER_MODULE, 'TRANSPORTER_MODULE'),
    )

    handler = models.CharField(max_length=200, null=True, choices=TYPE, default=STIR_FRY_MODULE)
    recipe_name = models.CharField(null=True, blank=True, max_length=400)
    recipe_author = models.CharField(null=True, blank=True, max_length=400)
    description = models.CharField(null=True, blank=True, max_length=400)
    image_path = models.ImageField(upload_to=upload_recipe_image, null=True, blank=True)
    cook_counts = models.IntegerField(default=0)
    etc = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=19, decimal_places=2)
    cv_model_path = models.CharField(null=True, blank=True, max_length=400)
    number_of_class = models.IntegerField(default=0)
    cv_images_path = models.CharField(max_length=800, null=True)

    def __str__(self):
        return self.recipe_name


class CookState(DocumentModel):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                  default=None, blank=True, null=True,
                                  related_name="cook_states_of_recipe", )
    state_label = models.CharField(null=True, blank=True, max_length=400)
    state_name = models.CharField(null=True, blank=True, max_length=400)


class StockGroup(DocumentModel):
    group_name = models.CharField(null=True, blank=True, max_length=400)
    color = models.CharField(null=True, blank=True, max_length=400)


class Coordinates(DocumentModel):
    SOLID = 'SOLID'
    GRANULAR = 'GRANULAR'
    LIQUID = 'LIQUID'

    TYPE = (
        (SOLID, 'SOLID'),
        (GRANULAR, 'GRANULAR'),
        (LIQUID, 'LIQUID'),
    )
    type = models.CharField(max_length=200, null=True, choices=TYPE, default=None)
    name = models.CharField(max_length=200, default=None)
    linear = models.IntegerField(default=0, null=True, blank=True, )
    center = models.IntegerField(default=0, null=True, blank=True, )
    ordinal = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} {self.linear} {self.center} {self.ordinal}'


class Ingredient(DocumentModel):
    GRAM = 'GRAM'
    KILOGRAM = 'KILOGRAM'
    TABLE_SPOON = 'TABLE_SPOON'
    TEA_SPOON = 'TEA_SPOON'
    MILLILITER = 'MILLILITER'
    UNIT = (
        (GRAM, 'GRAM'),
        (KILOGRAM, 'KILOGRAM'),
        (TABLE_SPOON, 'TABLE_SPOON'),
        (MILLILITER, 'MILLILITER'),
    )

    SOLID = 'SOLID'
    GRANULAR = 'GRANULAR'
    LIQUID = 'LIQUID'

    TYPE = (
        (SOLID, 'SOLID'),
        (GRANULAR, 'GRANULAR'),
        (LIQUID, 'LIQUID'),
    )

    ingredient_name = models.CharField(null=True, blank=True, max_length=400)
    stock_count = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    coordinate_x = models.IntegerField(default=0)
    coordinate_y = models.IntegerField(default=0)
    coordinate_id = models.ForeignKey(Coordinates, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                      related_name="ingredients_of_group", )
    image_path = models.ImageField(upload_to=upload_ingredient_image, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, choices=TYPE, default=None)
    unit = models.CharField(max_length=200, null=True, choices=UNIT, default=None)
    invoked_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.ingredient_name} {self.id}'


class Instruction(DocumentModel):
    COOK = 'COOK'
    PICK_INGREDIENT = 'PICK_INGREDIENT'
    PORTION_FOOD = 'PORTION_FOOD'
    MIX_FOOD = 'MIX_FOOD'
    PUMP_WATER = 'PUMP_WATER'
    SET_TO_TEMPERATURE = 'SET_TO_TEMPERATURE'

    NAME = (
        (COOK, 'COOK'),
        (PICK_INGREDIENT, 'PICK_INGREDIENT'),
        (PORTION_FOOD, 'PORTION_FOOD'),
        (MIX_FOOD, 'MIX_FOOD'),
        (PUMP_WATER, 'PUMP_WATER'),
        (SET_TO_TEMPERATURE, 'SET_TO_TEMPERATURE'),
    )
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=None,
                                  related_name="instructions_of_recipe", )
    name = models.CharField(max_length=200, choices=NAME, default=COOK)
    ordinal = models.IntegerField(default=0)
    target_temperature = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    duration = models.IntegerField(default=0, null=True)
    flip_enabled = models.BooleanField(default=False, null=True)
    volume = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    quantity = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    weight = models.DecimalField(max_digits=19, decimal_places=2, null=True)


class IngredientItem(DocumentModel):
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default=None,
                                      related_name="ingredient_items_referring_ingredient", )
    instruction_id = models.ForeignKey(Instruction, on_delete=models.CASCADE, default=None,
                                       related_name="ingredient_items_of_instruction", )

    quantity = models.IntegerField(default=0)


class Task(DocumentModel):
    QUEUE = 'QUEUE'
    PENDING = 'PENDING'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'
    COMPLETED = 'COMPLETED'

    TASK_STATUS = (
        (QUEUE, 'QUEUE'),
        (PENDING, 'PENDING'),
        (CANCELED, 'CANCELED'),
        (ERROR, 'ERROR'),
        (COMPLETED, 'COMPLETED'),
    )

    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE, default=0, related_name="tasks_on_recipe", )
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE, default=0, related_name="tasks_run_on_module", )
    task_name = models.CharField(null=True, blank=True, max_length=400)
    time_to_complete = models.IntegerField(default=0, null=True, blank=True, )
    task_status = models.CharField(max_length=200, null=True, choices=TASK_STATUS, default=QUEUE)
    failed_at = models.CharField(max_length=200, blank=True, null=True, default=None)
    last_success_job = models.CharField(max_length=200, blank=True, null=True, default=None)
    current_job = models.CharField(max_length=200, blank=True, null=True, default=None)


class Setting(DocumentModel):
    STRING = 'STRING'
    INT = 'INT'
    DOUBLE = 'DOUBLE'
    BOOLEAN = 'BOOLEAN'

    TYPE = (
        (STRING, 'STRING'),
        (INT, 'INT'),
        (DOUBLE, 'DOUBLE'),
        (BOOLEAN, 'BOOLEAN'),
    )

    key = models.CharField(null=True, blank=True, max_length=400)
    label = models.CharField(null=True, blank=True, max_length=400)
    string_value = models.CharField(null=True, blank=True, max_length=400)
    int_value = models.IntegerField(default=0, null=True, blank=True)
    double_value = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    bool_value = models.BooleanField(default=False, null=True)
    type = models.CharField(max_length=200, null=True, choices=TYPE, default=STRING)
