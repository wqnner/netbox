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
