from pdb import set_trace as st

from app.models.reagent_model import ReagentModel
from app.models.reagent_category_model import ReagentCategoryModel


class BatchReagentEntry():
    """
    Utility class to input multiple reagents into the database.
    """

    def __init__(self):
        pass

    def load_db(self, reagents):
        """
        Provide reagents strings and the category (string) they belong to like 
        this:

            reagents = (
                ('reagent_1', 'category_A'),
                ('reagent_2', 'category_A'),
                ('reagent_3', 'category_B'),
            )

        The categories will be created on-the-fly automatically if necessary.

        If pre-existing reagent names are encountered, these will be skipped,
        leaving the incumbent unaltered.
        """
        for reagent_name, category_str in reagents:
            if ReagentModel.objects.filter(name=reagent_name).exists():
                pass
            category_obj, newly_created = \
                ReagentCategoryModel.objects.get_or_create(name=category_str)
            ReagentModel.make(reagent_name, category_obj)
