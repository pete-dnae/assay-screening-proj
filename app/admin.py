from django.contrib import admin

from .models import Concentration
from .models import ConcreteReagent
from .models import BufferMix
from .models import MixedReagent
from .models import PlaceholderReagent
from .models import MasterMix
from .models import Gene
from .models import Organism
from .models import Primer
from .models import PrimerPair
from .models import PrimerKit
from .models import Arg
from .models import Strain
from .models import StrainKit
from .models import CyclingPattern
from .models import AllocRule
from .models import AllocationInstructions
from .models import Plate
from .models import Experiment

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

