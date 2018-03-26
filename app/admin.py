from django.contrib import admin

from .models.experiment_model import ExperimentModel
from .models.rules_script_model import RulesScriptModel
from .models.reagent_model import ReagentModel
from .models.reagent_category_model import ReagentCategoryModel
from .models.reagent_group_model import ReagentGroupModel
from .models.units_model import UnitsModel


admin.site.register(UnitsModel)
admin.site.register(ReagentModel)
admin.site.register(ReagentCategoryModel)
admin.site.register(ReagentGroupModel)
admin.site.register(RulesScriptModel)
admin.site.register(ExperimentModel)

