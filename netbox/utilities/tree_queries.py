from django.db.models import Manager
from django.db.models.expressions import RawSQL
from tree_queries.query import TreeManager as TreeManager_
from tree_queries.query import TreeQuerySet as TreeQuerySet_

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

    _with_tree_fields = False

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
        if cumulative:
            SQL = """
            WITH recursive __tree ( "tree_depth", "tree_path", "tree_pk" ) AS
            (
                  SELECT 0             AS tree_depth,
                         array[T1.id]  AS tree_path,
                         T1."id"
                   FROM "{table1}" T0
                  INNER JOIN "{table2}" T1
                     ON (T0."{rel_field}_id" = T1."id")
                  WHERE  T1."parent_id" IS NULL
                  UNION ALL
                  SELECT __tree.tree_depth + 1 AS tree_depth,
                         __tree.tree_path
                                || T1.id,
                         T1."id"
                   FROM "{table1}" T0
                  INNER JOIN "{table2}" T1
                     ON (T0."{rel_field}_id" = T1."id")
                  JOIN   __tree
                  ON     T1."parent_id" = __tree.tree_pk
            )
            SELECT count(*)
              FROM (
                    SELECT T0."id"
                      FROM "{table1}" T0
                     INNER JOIN "{table2}" T1
                        ON (T0."{rel_field}_id" = T1."id")
                     WHERE (T1.id = ANY(__tree.tree_path))
                   ) _count
            """

            params = {
                "table1": rel_model._meta.db_table,
                "table2": rel_model._meta.get_field(rel_field).remote_field.model._meta.db_table,
                "rel_field": rel_field,
            }

            return queryset.with_tree_fields().annotate(**{count_attr: RawSQL(SQL.format(**params), {})})
        else:
            current_rel_model = rel_model
            for rel_field_part in rel_field.split("__"):
                current_tree_field = current_rel_model._meta.get_field(rel_field_part)
                current_rel_model = current_tree_field.related_model
            tree_field = current_tree_field

            if isinstance(tree_field, ManyToManyField):
                field_name = "pk"
            else:
                field_name = tree_field.remote_field.field_name

            subquery_filters = {
                rel_field: OuterRef(field_name),
            }
        subquery = rel_model.objects.filter(**subquery_filters, **extra_filters).values("pk")
        return queryset.with_tree_fields().annotate(**{count_attr: SQCount(subquery)})
