# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Person.'''

from Acquisition import aq_parent
from eke.knowledge.content import knowledgeobject
from eke.site import ProjectMessageFactory as _
from eke.site.config import PROJECTNAME
from eke.site.interfaces import IPerson, ISite
from eke.site.utils import generateTitleFromNameComponents
from Products.Archetypes import atapi
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.utils import getToolByName
from Products.validation import V_REQUIRED
from zope.interface import implements, directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

PersonSchema = knowledgeobject.KnowledgeObjectSchema.copy() + atapi.Schema((
    atapi.StringField(
        'givenName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Given Name'),
            description=_(u'The name given to the person at birth and is oft considered the "first" name in Western societies.'),
        ),
        required=False,
        predicateURI='http://xmlns.com/foaf/0.1/givenname',
    ),
    atapi.StringField(
        'middleName',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Middle Name'),
            description=_(u'A secondary name given the person.'),
        ),
        required=False,
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#middleName',
    ),
    atapi.StringField(
        'surname',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Surname'),
            description=_(u'The family name oft inherited from birth parents and considered the "last" name in Western societies'),
        ),
        required=True,
        predicateURI='http://xmlns.com/foaf/0.1/surname',
    ),
    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Telephone Number'),
            description=_(u'The number at which the person may be reached via the Public Switched Telephone Network.'),
        ),
        required=False,
        predicateURI='http://xmlns.com/foaf/0.1/phone',
    ),
    atapi.StringField(
        'fax',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'FAX'),
            description=_(u'Facsimile telephone number.'),
        ),
        predicateURI='http://www.w3.org/2001/vcard-rdf/3.0#fax',
    ),
    atapi.StringField(
        'edrnTitle',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'EDRN Title'),
            description=_(u'Title or honorific given by the Early Detection Research Network.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#edrnTitle',
    ),
    atapi.StringField(
        'specialty',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Specialty'),
            description=_(u'Area of specialization taken by this person.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#specialty',
    ),
    atapi.StringField(
        'mbox',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Mail Box Address'),
            description=_(u'The address at which the person may receive electronic mail.'),
        ),
        required=False,
        predicateURI='http://xmlns.com/foaf/0.1/mbox',
    ),
    atapi.ImageField(
        'image',
        required=False,
        storage=atapi.AnnotationStorage(migrate=True),
        languageIndependent=True,
        max_size=zconf.ATNewsItem.max_image_dimension,
        sizes={
            'large'   : (768, 768),
            'preview' : (400, 400),
            'mini'    : (200, 200),
            'thumb'   : (128, 128),
            'tile'    :  (64, 64),
            'icon'    :  (32, 32),
            'listing' :  (16, 16),
        },
        validators=(('isNonEmptyFile', V_REQUIRED), ('checkNewsImageMaxSize', V_REQUIRED)),
        widget=atapi.ImageWidget(
            description=_(u'An image for this person, such as a photograph or mugshot.'),
            label=_(u'Image'),
            show_content_type=False,
        ),
    ),
    atapi.ComputedField(
        'title',
        searchable=True,
        required=False,
        expression='context._computeTitle()',
        accessor='Title',
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'investigatorStatus',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        default='staff',
        widget=atapi.StringWidget(
            label=_(u'Investigator'),
            description=_(u'Status of this person as an investigator or as a mere staff member.'),
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'memberType',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        modes=('view',),
        widget=atapi.StringWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'siteName',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        modes=('view',),
        widget=atapi.StringWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.StringField(
        'piUID',
        storage=atapi.AnnotationStorage(),
        searchable=False,
        required=False,
        widget=atapi.StringWidget(
            label=_(u'PI UID'),
            description=_(u'Unique identifier of the principal investigator of the site where this person works.'),
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),
))

finalizeATCTSchema(PersonSchema, folderish=False, moveDiscussion=False)

class Person(knowledgeobject.KnowledgeObject):
    '''Person.'''
    implements(IPerson)
    schema             = PersonSchema
    portal_type        = 'Person'
    givenName          = atapi.ATFieldProperty('givenName')
    middleName         = atapi.ATFieldProperty('middleName')
    surname            = atapi.ATFieldProperty('surname')
    phone              = atapi.ATFieldProperty('phone')
    fax                = atapi.ATFieldProperty('fax')
    edrnTitle          = atapi.ATFieldProperty('edrnTitle')
    specialty          = atapi.ATFieldProperty('specialty')
    mbox               = atapi.ATFieldProperty('mbox')
    investigatorStatus = atapi.ATFieldProperty('investigatorStatus')
    memberType         = atapi.ATFieldProperty('memberType')
    siteName           = atapi.ATFieldProperty('siteName')
    piUID              = atapi.ATFieldProperty('piUID')
    def _computeTitle(self):
        return generateTitleFromNameComponents((self.surname, self.givenName, self.middleName))
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)
    def __bobo_traverse__(self, REQUEST, name):
        """Give transparent access to image scales. This hooks into the
        low-level traversal machinery, checking to see if we are trying to
        traverse to /path/to/object/image_<scalename>, and if so, returns
        the appropriate image content.
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image
        return super(Person, self).__bobo_traverse__(REQUEST, name)
    def setInformationProvidedBySite(self):
        # Get our parent site obj; if we don't have one (or it's not a site but something weird like portal_factory)
        # then we can't do any updating.
        parent = aq_parent(self)
        if parent is None or not ISite.providedBy(parent): return
        # Update my attributes accordingly
        self.siteName, self.memberType, self.piUID = parent.title, parent.memberType, parent.piUID

atapi.registerType(Person, PROJECTNAME)

def PersonVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    # TODO: filter by review_state? Or by a specific site?
    results = catalog(
        object_provides=IPerson.__identifier__,
        sort_on='sortable_title'
    )
    items = [(u'%s (%s)' % (i.Title, i.siteID), i.UID) for i in results]
    return SimpleVocabulary.fromItems(items)
directlyProvides(PersonVocabularyFactory, IVocabularyFactory)

def PersonVocabularyWithNoReferenceFactory(context):
    terms = [i for i in PersonVocabularyFactory(context)]
    noReference = u'<no reference>' # FIXME: not i18n
    terms.insert(0, SimpleTerm('', noReference))
    return SimpleVocabulary(terms)
directlyProvides(PersonVocabularyWithNoReferenceFactory, IVocabularyFactory)

def PrincipalInvestigatorVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    results = catalog(object_provides=IPerson.__identifier__, investigatorStatus='pi')
    items = {}
    for i in results:
        if i.Title not in items:
            items[i.Title] = []
        uidsForName = items[i.Title]
        uidsForName.append(i.UID)
    terms = []
    for name, uids in items.iteritems():
        if len(uids) == 1:
            terms.append((name, uids[0]))
        elif len(uids) > 1:
            index = 1
            for uid in uids:
                terms.append((u'%s (%d)' % (name, index), uid))
                index += 1
    terms.sort()
    return SimpleVocabulary.fromItems(terms)
directlyProvides(PrincipalInvestigatorVocabularyFactory, IVocabularyFactory)

def NotPeonsVocabularyFactory(context):
    peon, notPeon, pi = u'Staff', u'Investigator', u'PI' # FIXME: not i18n
    return SimpleVocabulary.fromItems(((pi, 'pi'), (notPeon, 'investigator'), (peon, 'staff')))
directlyProvides(NotPeonsVocabularyFactory, IVocabularyFactory)

def setSiteInformation(context, event):
    if IPerson.providedBy(context): # should always be true
        context.setInformationProvidedBySite()
