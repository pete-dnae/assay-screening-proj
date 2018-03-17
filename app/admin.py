from django.contrib import admin

from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel


admin.site.register(RulesScriptModel)
admin.site.register(ExperimentModel)

