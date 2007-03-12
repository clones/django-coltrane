from django.conf import settings
from django.core.signals import pre_save
from django.dispatch import dispatcher
from django.contrib.comments.models import Comment, FreeComment
from django.contrib.sites.models import Site
from akismet import Akismet

def moderate_comments(sender, instance):
    """
    Applies comment moderation to newly-posted comments.
    
    Moderation happens in two phases:
    
        1. If the object the comment is being posted on has a method
           named ``comments_open``, it will be called; if the return
           value evaluates to ``False, the comment's ``is_public``
           field will be set to ``False`` and no further processing
           will be done.
    
        2. If the object did not have a ``comments_open`` method, or
           if that method's return value evaluated to ``True``, then
           the comment will be submitted to Akismet for a spam check,
           and if Akismet thinks the comment is spam, then its
           ``is_public`` field will be set to ``False``.
    
    """
    if not instance.id: # Only check when the comment is first saved.
        content_object = instance.get_content_object()
        comments_open = getattr(content_object, 'comments_open', None)
        if callable(comments_open) and not comments_open():
            instance.is_public = False
        elif hasattar(settings, 'AKISMET_API_KEY') and settings.AKISMET_API_KEY:
            akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                                  blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                 'referrer': '',
                                 'user_ip': instance.ip_address,
                                 'user_agent': '' }
                if akismet_api.comment_check(instance.comment, data=akismet_data, build_data=True):
                    instance.is_public = False

dispatcher.connect(moderate_comments, sender=Comment, signal=pre_save)
dispatcher.connect(moderate_comments, sender=FreeComment, signal=pre_save)

def apply_markup_filter(text):
    """
    Applies a text-to-HTML conversion function to a piece of text and returns
    the generated HTML.
    
    The function to use is derived from the value of the setting ``MARKUP_FILTER``,
    which should be a 2-tuple:
    
        * The first element should be the name of a markup filter -- e.g.,
          "markdown" -- to apply. If no markup filter is desired, set this to
          None.
    
        * The second element should be a dictionary of keyword arguments which will be
          passed to the markup function. If no extra arguments are desired, set this
          to an empty dictionary; some arguments may still be inferred as needed,
          however.
    
    So, for example, to use Markdown with safe mode turned on (safe mode removes raw
    HTML), put this in your settings file::
    
        MARKUP_FILTER = ('markdown', { 'safe_mode': True })
    
    Currently supports Textile, Markdown and reStructuredText, using names identical
    to the template filters found in ``django.contrib.markup``.
    
    """
    markup_func_name = settings.MARKUP_FILTER[0]
    markup_kwargs = settings.MARKUP_FILTER[1]    
    
    if markup_func_name is None: # No processing is needed.
        return text
    
    if markup_func_name not in ('textile', 'markdown', 'restructuredtext'):
        raise ValueError("'%s' is not a valid value for the first element of MARKUP_FILTER; \
                          acceptable values are 'textile', 'markdown', 'restructuredtext' and None" % markup_func_name)
    
    if markup_func_name == 'textile':
        import textile
        if not 'encoding' in markup_kwargs:
            markup_kwargs.update(encoding=settings.DEFAULT_CHARSET)
        if not 'output' in markup_kwargs:
            markup_kwargs.update(output=settings.DEFAULT_CHARSET)
        return textile.textile(text, **markup_kwargs)
    
    elif markup_func_name == 'markdown':
        import markdown
        return markdown.markdown(text, **markup_kwargs)
    
    elif markup_func_name == 'restructuredtext':
        from docutils import core
        markup_func = core.publish_parts
        if not 'settings_overrides' in markup_kwargs:
            markup_kwargs.update(settings_overrides=getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {}))
        if not 'writer_name' in markup_kwargs:
            markup_kwargs.update(writer_name='html4css1')
        parts = publish_parts(source=text, **markup_kwargs)
        return parts['fragment']
