from django.db import models

def most_commented(self, num=5, free=True):
    """
    Returns the ``num`` Entries with the highest comment counts,
    in order.

    Pass ``free=False`` if you're using the registered comment
    model (``Comment``) instead of the anonymous comment model
    (``FreeComment``).

    """
    from django.db import backend, connection
    from django.contrib.comments import models as comment_models
    from django.contrib.contenttypes.models import ContentType
    if free:
        comment_opts = comment_models.FreeComment._meta
    else:
        comment_opts = comment_models.Comment._meta
    ctype = ContentType.objects.get_for_model(self.model)
    query = """SELECT %s, COUNT(*) AS score
    FROM %s
    WHERE content_type_id = %%s
    AND is_public = 1
    GROUP BY %s
    ORDER BY score DESC""" % (backend.quote_name('object_id'),
                              backend.quote_name(comment_opts.db_table),
                              backend.quote_name('object_id'),)

    cursor = connection.cursor()
    cursor.execute(query, [ctype.id])
    entry_ids = [row[0] for row in cursor.fetchall()[:num]]

    # Use ``in_bulk`` here instead of an ``id__in`` filter, because ``id__in``
    # would clobber the ordering.
    entry_dict = self.in_bulk(entry_ids)
    return [entry_dict[entry_id] for entry_id in entry_ids]


class LiveEntryManager(models.Manager):
    """
    Custom manager for the Entry model, providing shortcuts for
    filtering by entry status.
    
    """
    def featured(self):
        """
        Returns a ``QuerySet`` of featured Entries.
        
        """
        return self.filter(featured__exact=True)
        
    def get_query_set(self):
        """
        Overrides the default ``QuerySet`` to only include Entries
        with a status of 'live'.
        
        """
        return super(LiveEntryManager, self).get_query_set().filter(status__exact=1)

    def latest_featured(self):
        """
        Returns the latest featured Entry if there is one, or ``None``
        if there isn't.
        
        """
        try:
            return self.featured()[0]
        except IndexError:
            return None
    
    most_commented = most_commented


class LinksManager(models.Manager):
    most_commented = most_commented
