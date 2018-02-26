from django.contrib import admin

from .models.experiment_model import *
from .models.reagent_models import *
from .models.primer_models import *
from .models.strain_models import *
from .models.rule_models import *


admin.site.register(Composition)
admin.site.register(Measure)
admin.site.register(Gene)
admin.site.register(Organism)
admin.site.register(Primer)
admin.site.register(PrimerPair)
admin.site.register(Arg)
admin.site.register(Strain)
admin.site.register(CyclingPattern)
admin.site.register(Experiment)

