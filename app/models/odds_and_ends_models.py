from django.db import models

def mk_choices(items):
    """
    Utility to reduce typing when making 2-tuple lists required by
    model.choices.
    """
    return ((i,i) for i in items)


def smart_deep_copy_model(model):
    """
    Capable of making a replica of the given model instance in the database
    and returning it. Operates recursively, to also make copies of fields
    referred to by foreign keys and by many to many fields, so that these do
    not become unwittingly shared by the copies. (Like Python's deepcopy).
    """
    # Do the standard trick to create a new database instance with a new id,
    model.pk = None
    model.save()

    # We can now treat the model as the new on under construction and it has
    # the new pk field that will be used for example by many to many field
    # operations.

    # Recursivly copy the foreign key fields, and many to many fields

    # Freeze the existing field objects outside the loop because we mutate them
    # inside the loop..
    fields = [f for f in model._meta.get_fields()]
    for field in fields:
        name = field.name
        if isinstance(field, models.ForeignKey):
            foreign_object = getattr(model, name)   
            if foreign_object:
                duplicate = smart_deep_copy_model(foreign_object) # Recurses.
                setattr(model, name, duplicate)   
        elif isinstance(field, models.ManyToManyField):
            manager = getattr(model, name)
            foreign_objects = manager.all()
            manager.clear()
            for foreign_object in foreign_objects:
                duplicate = smart_deep_copy(foreign_object) # Recurse.
                manager.add(duplicate)
    # Finish off by saving the changes to the model and returning the model
    # object.
    model.save()
    return model


class CyclingPattern(models.Model):
    """
    A little lost model with no home to go to.
    """
    activation_time = models.PositiveIntegerField()
    activation_temp = models.PositiveIntegerField()
    num_cycles = models.PositiveIntegerField()
    denature_temp = models.PositiveIntegerField()
    denature_time = models.PositiveIntegerField()
    anneal_temp = models.PositiveIntegerField()
    anneal_time = models.PositiveIntegerField()
    extend_temp = models.PositiveIntegerField()
    extend_time = models.PositiveIntegerField()
