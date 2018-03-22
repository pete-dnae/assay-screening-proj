from django.contrib import admin

from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel
from .models.reagent_name_model import ReagentNameModel
from .models.reagent_category_model import ReagentCategoryModel
from .models.units_model import UnitsModel


admin.site.register(UnitsModel)
admin.site.register(ReagentNameModel)
admin.site.register(ReagentCategoryModel)
admin.site.register(RulesScriptModel)
admin.site.register(ExperimentModel)

