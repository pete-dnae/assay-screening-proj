from app.models.reagent_model import ReagentModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.units_model import UnitsModel
from collections import defaultdict
class ViewHelpers:
    """
    A place to put non-trivial code needed to provide view functionality, so
    that the main *views.py* module can remain essentially just a list of
    views.
    """

    @classmethod
    def all_allowed_names(cls):
        """
        Provides a data structure that lists all the reagent names available,
        all the group names available, and all the units.
        """
        reagent_names = cls.reagent_names()
        group_names = cls.group_names()
        combined = sorted(reagent_names + group_names)

        return {
            'reagents_and_groups': combined,
            'units': cls.units(),
        }

    @classmethod
    def reagent_names(cls):
        """
        Provides a list of all available reagent names.
        """
        names = [r.name for r in ReagentModel.objects.all()]
        return names

    @classmethod
    def group_names(cls):
        """
        Provides a list of all available group names.
        """
        names = set()
        for group in ReagentGroupModel.objects.all():
            names.add(group.group_name)
        return list(names)
        
    @classmethod
    def units(cls):
        """
        Provides a list of all available units.
        """
        abbrev = [u.abbrev for u in UnitsModel.objects.all()]
        return sorted(abbrev)

    @classmethod
    def reagents_category(cls):
        """
        Provides a dict with reagent names as keys and reagent category as
        value
        """
        reagents_category = {r.name: r.category.name
                           for r in ReagentModel.objects.all()}

        return reagents_category
    @classmethod
    def reagent_groups_category(cls):
        """
        provides a dictionary with reagent group name as keys and reagent
        group category as value
        category of the first reagent in the group is assigned as the reagent
        group's category
        """
        group_category = {}
        group_names = cls.group_names()
        for group_name in group_names:
            group_record= ReagentGroupModel.objects.filter\
                (group_name=group_name).first()
            group_category[group_name] = group_record.reagent.category.name
        return group_category

    @classmethod
    def available_reagents_category(cls):
        """
        Combines and returns reagents and reagent groups categories
        """

        return {**cls.reagents_category(), **cls.reagent_groups_category()}
