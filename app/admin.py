from django.contrib import admin

from .models.experiment_model import *
from .models.reagent_models import *
from .models.primer_models import *
from .models.strain_models import *
from .models.plate_models import *

admin.site.register(Concentration)
admin.site.register(ConcreteReagent)
admin.site.register(BufferMix)
admin.site.register(MixedReagent)
admin.site.register(PlaceholderReagent)
admin.site.register(MasterMix)
admin.site.register(Gene)
admin.site.register(Organism)
admin.site.register(Primer)
admin.site.register(PrimerPair)
admin.site.register(PrimerKit)
admin.site.register(Arg)
admin.site.register(Strain)
admin.site.register(StrainKit)
admin.site.register(CyclingPattern)
admin.site.register(AllocRule)
admin.site.register(AllocationInstructions)
admin.site.register(Plate)
admin.site.register(Experiment)
admin.site.register(Allocatable)

