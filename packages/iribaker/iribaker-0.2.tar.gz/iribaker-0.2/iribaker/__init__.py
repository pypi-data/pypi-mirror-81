import urllib.parse
import rfc3987
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


def to_iri(iri):
    """
    Safely quotes an IRI in a way that is resilient to unicode and incorrect
    arguments (checks for RFC 3987 compliance and falls back to percent encoding)
    """
    try:
        # If we can safely parse the URI, then we don't
        # need to do anything special here
        rfc3987.parse(iri, rule='IRI')
        logger.debug("This is already a valid IRI, doing nothing...")
        return iri
    except:
        # The URI is not valid, so we'll have to fix it.
        logger.debug("The IRI is not valid, proceeding to quote...")
        # First see whether we can actually parse it *as if* it is a URI

        parts = urllib.parse.urlsplit(iri)
        if not parts.scheme or not parts.netloc:
            # If there is no scheme (e.g. http) nor a net location (e.g.
            # example.com) then we cannot do anything
            logger.error("The argument you provided does not comply with "
                         "RFC 3987 and is not parseable as a IRI"
                         "(there is no scheme or no net location part)")
            logger.error(iri)
            raise Exception("The argument you provided does not comply with"
                            "RFC 3987 and is not parseable as a IRI"
                            "(there is no scheme or no net location part)")

        logger.debug("The IRI contains all necessary parts (scheme + net location)")
        quoted_parts = {}
        # We'll now convert the path, query and fragment parts of the URI

        # Get the 'anti-pattern' for the valid characters (see rfc3987 package)
        # This is roughly the ipchar pattern plus the '/' as we don't need to match
        # the entire path, but merely the individual characters
        no_invalid_characters = rfc3987.get_compiled_pattern("(?!%(iunreserved)s|%(pct_encoded)s|%(sub_delims)s|:|@|/)(.)")

        # Replace the invalid characters with an underscore (no need to roundtrip)
        quoted_parts['path'] = no_invalid_characters.sub('_', parts.path)
        if parts.fragment:
            quoted_parts['fragment'] = no_invalid_characters.sub('_', parts.fragment)
        if parts.query:
            quoted_parts['query'] = urllib.parse.quote(parts.query.encode('utf-8'),safe="&=")
        # Leave these untouched
        quoted_parts['scheme'] = parts.scheme
        quoted_parts['authority'] = parts.netloc

        # Extra check to make sure we now have a valid IRI
        quoted_iri = rfc3987.compose(**quoted_parts)
        try:
            rfc3987.parse(quoted_iri)
        except:
            # Unable to generate a valid quoted iri, using the straightforward
            # urllib percent quoting (but this is ugly!)
            logger.warning('Could not safely quote as IRI, falling back to '
                           'percent encoding')
            quoted_iri = urllib.parse.quote(iri.encode('utf-8'))

        return quoted_iri
