from tree_queries.query import TreeManager as TreeManager_
from tree_queries.query import TreeQuerySet as TreeQuerySet_

from django.db.models import Manager
from .querysets import RestrictedQuerySet

__all__ = (
    'TreeManager',
    'TreeQuerySet',
)


class TreeQuerySet(TreeQuerySet_, RestrictedQuerySet):
    """
    Mate django-tree-queries TreeQuerySet with our RestrictedQuerySet for permissions enforcement.
    """
    pass


class TreeManager(Manager.from_queryset(TreeQuerySet), TreeManager_):
    """
    Extend django-tree-queries TreeManager to incorporate RestrictedQuerySet().
    """

    _with_tree_fields = True

    def add_related_count(
        self,
        queryset,
        rel_model,
        rel_field,
        count_attr,
        cumulative=False,
        extra_filters={},
    ):
        """
        Adds a related item count to a given ``QuerySet`` using its
        ``extra`` method, for a ``Model`` class which has a relation to
        this ``Manager``'s ``Model`` class.

        Arguments:

        ``rel_model``
           A ``Model`` class which has a relation to this `Manager``'s
           ``Model`` class.

        ``rel_field``
           The name of the field in ``rel_model`` which holds the
           relation.

        ``count_attr``
           The name of an attribute which should be added to each item in
           this ``QuerySet``, containing a count of how many instances
           of ``rel_model`` are related to it through ``rel_field``.

        ``cumulative``
           If ``True``, the count will be for each item and all of its
           descendants, otherwise it will be for each item itself.

        ``extra_filters``
           Dict with aditional parameters filtering the related queryset.
        """
        return queryset
