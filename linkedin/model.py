import datetime

from xml.sax.saxutils import unescape

def get_child(node, tagName,default=None):
    try:
        domNode = node.getElementsByTagName(tagName)[0]
        childNodes = domNode.childNodes
        if childNodes:
            return childNodes[0].nodeValue
        return default
    except:
        return default

def get_child_xml(node,tag_name,default=None):
    try:
        domNode = node.find(tag_name)
        if domNode is not None:
            return domNode.text
        else:
            return default
    except:
        return default

def str_to_bool(s):
    if s is None:
        return None
    if s.lower() == "true":
        return True
    elif s.lower() == "false":
        return False
    else:
        return None

def parse_date(node):
    year = int(get_child(node, "year"))
    month = get_child(node, "month")
    if month:
        month = int(month)
    else:
        month = 1
    return datetime.date(year, month, 1)

def parse_connections(connections_node):
    connections_list = []
    connections = connections_node.getElementsByTagName("connection")
    if connections:
        for connection in connections:
            person = connection.getElementsByTagName("person")
            if person:
                person = person[0]
                connections_list.append(Profile.create(person))

    return connections_list

class LinkedInModel:

    def __repr__(self):
        d = {}
        for x,y in self.__dict__.items():
            if (self.__dict__[x]):
                d[x] = y
        return (self.__module__ + "." + self.__class__.__name__ + " " +
                d.__repr__())

class Publication(LinkedInModel):

    def __init__(self):
        self.id = None
        self.title = None
        self.publisher_name = None
        self.date = None
        self.url = None
        self.summary = None
        # Notice that we are ignoring authors field for now until someone will need it.

    @staticmethod
    def create(node):
        """
        <publication>
            <id>3</id>
            <title>Publication list, with links to individual papers</title>
            <publisher>
                <name>Iftach</name>
            </publisher>
            <date>
                <year>2005</year>
                <month>5</month>
            </date>
            <url>URLURL</url>
            <summary>My summary</summary>
        </publication>
        """
        publication = Publication()
        publication.id = get_child(node, "id")
        publication.title = get_child(node, "title")

        publisher = node.getElementsByTagName("publisher")
        if publisher:
            publication.publisher_name = get_child(publisher[0], "name")

        date = node.getElementsByTagName("date")
        if date:
            publication.date = parse_date(date[0])

        publication.url = get_child(node, "url")
        publication.summary = get_child(node, "summary")
        return publication

class Company(LinkedInModel):

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.size = None
        self.industry = None
        self.ticker = None

    @staticmethod
    def create(node):
        """
        <company>
        <id>1009</id>
        <name>XIV - IBM</name>
        <type>Public Company</type>
        <size>123</size>
        <industry>Information Technology and Services</industry>
        <ticker>IBM</ticker>
        </company>
        """
        company = Company()
        company.id = get_child(node, "id")
        company.name = get_child(node, "name")
        company.type = get_child(node, "type")
        company.size = get_child(node, "size")
        company.industry = get_child(node, "industry")
        company.ticker = get_child(node, "ticker")
        return company

class Education(LinkedInModel):
    """
    Class that wraps an education info of a user
    """
    def __init__(self):
        self.id          = None
        self.school_name = None
        self.degree      = None
        self.start_date  = None
        self.end_date    = None
        self.activities  = None
        self.notes       = None
        self.field_of_study = None

    @staticmethod
    def create(node):
        """
        <educations total="">
         <education>
          <id>
          <school-name>
          <degree>
          <start-date>
           <year>
          </start-date>
          <end-date>
           <year>
          </end-date>
         </education>
        </educations>
        """
        children = node.getElementsByTagName("education")
        result = []
        for child in children:
            education = Education()
            education.id = education._get_child(child, "id")
            education.activities = education._get_child(child, "activities")
            education.notes = education._get_child(child, "notes")
            education.school_name = education._get_child(child, "school-name")
            education.degree = education._get_child(child, "degree")
            education.field_of_study = education._get_child(child, "field-of-study")

            start_date = child.getElementsByTagName("start-date")
            if start_date:
                education.start_date = parse_date(start_date[0])

            end_date = child.getElementsByTagName("end-date")
            if end_date:
                education.end_date = parse_date(end_date[0])

            result.append(education)
        return result

    def _get_child(self, node, tagName):
        try:
            domNode = node.getElementsByTagName(tagName)[0]
            childNodes = domNode.childNodes
            if childNodes:
                return childNodes[0].nodeValue
            return None
        except:
            return None

class Position(LinkedInModel):
    """
    Class that wraps a business position info of a user
    """
    def __init__(self):
        self.id         = None
        self.title      = None
        self.summary    = None
        self.start_date = None
        self.end_date   = None
        self.company    = None
        self.is_current = None


    @staticmethod
    def create(node):
        """
         <position>
          <id>101526695</id>
          <title>Developer</title>
          <summary></summary>
          <start-date>
          <year>2009</year>
          <month>9</month>
          </start-date>
          <is-current>true</is-current>
          <company>
            <name>Akinon</name>
          </company>
         </position>
        """
        position = Position()
        position.id = get_child(node, "id")
        position.title = get_child(node, "title")
        position.summary = get_child(node, "summary")
        position.is_current = str_to_bool(get_child(node, "is-current"))

        company = node.getElementsByTagName("company")
        if company:
            position.company = Company.create(company[0])

        start_date = node.getElementsByTagName("start-date")
        if start_date:
            position.start_date = parse_date(start_date[0])

        end_date = node.getElementsByTagName("end-date")
        if end_date:
            position.end_date = parse_date(end_date[0])

        return position

class Location(LinkedInModel):
    def __init__(self):
        self.name = None
        self.country_code = None

    @staticmethod
    def create(node):
        """
        <location>
            <name>
            <country>
                <code>
            </country>
        </location>
        """
        loc = Location()
        loc.name = get_child(node, "name")
        country = node.getElementsByTagName("country")
        if country:
            country = country[0]
            loc.country_code = get_child(country, "code")

        return loc

class RelationToViewer(LinkedInModel):
    def __init__(self):
        self.distance = None
        self.num_related_connections = None
        self.connections = []

    @classmethod
    def create(cls, node):
        """
        <relation-to-viewer>
            <distance>1</distance>
            <connections total="36" count="10" start="0">
                <connection>
                    <person>
                        <id>_tQbzI5kEk</id>
                        <first-name>Michael</first-name>
                        <last-name>Green</last-name>
                    </person>
                </connection>
            </connections>
        </relation-to-viewer>
        """
        relation = RelationToViewer()
        relation.distance = int(get_child(node, "distance"))
        relation.num_related_connections = int(get_child(node, "num-related-connections"))

        connections = node.getElementsByTagName("connections")
        if connections:
            connections = connections[0]
            if not relation.num_related_connections:
                if connections.hasAttribute("total"):
                    relation.num_related_connections = int(connections.attributes["total"].value)

            relation.connections = parse_connections(connections)

        return relation

class Profile(LinkedInModel):
    """
    Wraps the data which comes from Profile API of LinkedIn.
    For further information, take a look at LinkedIn Profile API.
    """
    def __init__(self):
        self.id          = None
        self.first_name  = None
        self.last_name   = None
        self.headline    = None
        self.location    = None
        self.industry    = None
        self.distance    = None
        self.relation_to_viewer = None
        self.summary     = None
        self.specialties = None
        self.proposal_comments = None
        self.associations = None
        self.interests   = None
        self.honors      = None
        self.public_url  = None
        self.private_url = None
        self.picture_url = None
        self.current_status = None
        self.current_share = None
        self.num_connections = None
        self.num_connections_capped = None
        self.languages   = []
        self.skills      = []
        self.connections = []
        self.positions   = []
        self.educations  = []
        self.xml_string  = None

    @staticmethod
    def create(node, debug=False):
        person = node
        if person.nodeName != "person":
            person = person.getElementsByTagName("person")[0]
        profile = Profile()
        profile.id = get_child(person, "id")
        profile.first_name = get_child(person, "first-name")
        profile.last_name = get_child(person, "last-name")
        profile.headline = get_child(person, "headline")
        profile.distance = get_child(person, "distance")
        profile.specialties = get_child(person, "specialties")
        profile.proposal_comments = get_child(person, "proposal-comments")
        profile.associations = get_child(person, "associations")
        profile.industry = get_child(person, "industry")
        profile.honors = get_child(person, "honors")
        profile.interests = get_child(person, "interests")
        profile.summary = get_child(person, "summary")
        profile.picture_url = profile._unescape(get_child(person, "picture-url"))
        profile.current_status = get_child(person, "current-status")
        profile.current_share = get_child(person, "current-share")
        profile.num_connections = get_child(person, "num-connections")
        profile.num_connections_capped = get_child(person, "num-connections-capped")
        profile.public_url = profile._unescape(get_child(person, "public-profile-url"))

        location = person.getElementsByTagName("location")
        if location:
            profile.location = Location.create(location[0])

        relation_to_viewer = person.getElementsByTagName("relation-to-viewer")
        if relation_to_viewer:
            relation_to_viewer = relation_to_viewer[0]
            profile.relation_to_viewer = RelationToViewer.create(relation_to_viewer)

        # Create connections
        connections = person.getElementsByTagName("connections")
        if connections:
            connections = connections[0]
            if not profile.num_connections and connections.hasAttribute("total"):
                profile.num_connections = int(connections.attributes["total"].value)
            profile.connections = parse_connections(connections)

        # create positions
        positions = person.getElementsByTagName("positions")

        if positions:
            positions = positions[0]
            positions = positions.getElementsByTagName("position")
            # TODO get the total
            for position in positions:
                profile.positions.append(Position.create(position))

        # TODO Last field working on is - publications

        private_profile = person.getElementsByTagName("site-standard-profile-request")
        if private_profile:
            private_profile = private_profile[0]
        profile.private_url = get_child(private_profile, "url")

        # create skills
        skills = person.getElementsByTagName("skills")
        if skills:
            skills = skills[0]
            children = skills.getElementsByTagName('skill')
            for child in children:
                if not child.getElementsByTagName('id'):
                    profile.skills.append(get_child(child, 'name'))

        # create languages
        languages = person.getElementsByTagName("languages")
        if languages:
            languages = languages[0]
            children = languages.getElementsByTagName('language')
            for child in children:
                if not child.getElementsByTagName('id'):
                    profile.languages.append(get_child(child, 'name'))

        # create educations
        educations = person.getElementsByTagName("educations")
        if educations:
            educations = educations[0]
            profile.educations = Education.create(educations)

        # For debugging
        if debug:
            profile.xml_string = node.toxml()

        return profile

    def _unescape(self, url):
        if url:
            return unescape(url)
        return url

def create_person_attrs(update,person,field="person"):
    name = "%s %s"%(get_child_xml(person,"first-name"),get_child_xml(person,"last-name"))
    setattr(update,u"%s_name"%field,name)
    id = get_child_xml(person,"id",None)
    setattr(update,"%s_id"%field,id)
    public_url = get_child_xml(person.find("site-standard-profile-request"),"url")
    setattr(update,"%s_public_url"%field,public_url)
    headline = get_child_xml(person,"headline")
    setattr(update,"%s_headline"%field,headline)
    return update

class CONN(object):
    """
    CONN updates contain a update-content/connections node that describe the member that was recently connected to. update-content/person indicates the first degree connection making the new connection.
    "John Irving is now connected to Paul Auster."
    """
    def __init__(self):
        self.person1_name = None # first name + last name
        self.person1_id = None
        self.person1_public_url = None
        self.person1_headline = None
        self.person2_name = None
        self.person2_id = None
        self.person2_public_url = None
        self.person2_headline = None

    @staticmethod
    def create(xml_element):
        update = CONN()
        content = xml_element.find("person")
        update = create_person_attrs(update,content,field="person1")
        person2 = content.find("connections").find("person")
        update = create_person_attrs(update,person2,field="person2")
        return update

    def __str__(self):
        return "%s is now connected to %s" % (self.person1_name.encode('utf8'),self.person2_name.encode('utf8'))


class NCON(object):
    """
    NCON updates contain a update-content/person node describing the member who recently became a connection to the requestor.
    "John Irving is now a connection."
    """
    def __init__(self):
        self.person_name = None # first name + last name
        self.person_id = None
        self.person_public_url = None
        self.person_headline = None

    @staticmethod
    def create(xml_element):
        update = NCON()
        content = xml_element.find("person")
        update = create_person_attrs(update,content,field="person1")
        return update

    def __str__(self):
        return "%s is now a connection."%self.person_name.encode('utf8')

class CCEM(object):
    """
    CCEM updates are infrequent updates where the requestor has someone in their uploaded address book who has just recently became a member of LinkedIn. They aren't necessarily connected to this individual yet, but it is likely they'll want to connect. The update-content/person node in this update indicates the recent LinkedIn member.
    "Gertrude Stein has joined LinkedIn."
    """
    def __init__(self):
        self.person_name = None # first name + last name
        self.person_id = None
        self.person_public_url = None
        self.person_headline = None

    @staticmethod
    def create(xml_element):
        update = CCEM()
        content = xml_element.find("person")
        update = create_person_attrs(update,content,field="person1")
        return update

    def __str__(self):
        return "%s has joined LinkedIn"%self.person_name.encode('utf8')

class SHAR(object):
    """
    Share updates are generated when a member shares or reshares an item. Shares are a more sophisticated form of status updates. They can contain text, but also an optional URL and photo. In general, you should expect at least a comment or a URL, or both, but neither one is mandatory if the other is provided.
    """
    def __init__(self):
        self.sharer_name = None
        self.sharer_id = None
        self.sharer_headline = None
        self.sharer_public_url = None

        self.original_sharer_name = None
        self.original_sharer_id = None
        self.original_sharer_headline = None

        self.share_id = None
        self.share_timestamp = None
        self.share_comment = None
        self.share_content_url = None
        self.share_content_title = None
        self.share_service_provider = None
        self.share_application = None
        self.share_pic_url = None

    @staticmethod
    def create(xml_element):
        update = SHAR()
        content = xml_element.find("person")
        update = create_person_attrs(update,content,field="sharer")
        update.share_pic_url = get_child_xml(content,"picture-url")
        cur_share = content.find("current-share")
        update = create_person_attrs(update,cur_share,field="original_sharer")
        update.share_id = "%s"%cur_share.find("id").text
        update.share_timestamp = "%s"%cur_share.find("timestamp").text
        update.share_comment = "%s"%cur_share.find("comment").text
        update.share_content_url = "%s"%cur_share.find("content").find("submitted-url").text
        update.share_content_title = "%s"%cur_share.find("content").find("title").text
        update.share_service_provider = "%s"%cur_share.find("source").find("service-provider").find("name").text
        update.share_application = "%s"%cur_share.find("source").find("application").find("name").text
        return update

    def __str__(self):
        share = self.share_pic_url if self.share_pic_url != '' and self.share_pic_url is not None else self.share_content_url
        return "%s shared %s. Originally shared by %s"%(self.sharer_name.encode('utf8'),share,self.original_sharer.encode('utf8'))

class STAT(object):
    """
    Status Updates are the result of first degree connections setting their status. While update-content/person will (as always) tell you about the member who made the update, update-content/person/current-status will contain the actual string the member has their status updated to. These strings will frequently contain URLs and are frequently HTML entity-encoded.
    "Taylor Singletary helping developers http://developers.linkedin.com"
    """
    def __init__(self):
        self.person_name = None
        self.person_id = None
        self.person_headline = None
        self.person_public_url = None
        self.current_status = None

    @staticmethod
    def create(xml_element):
        update = STAT()
        content = xml_element.find("person")
        update = create_person_attrs(update,content)
        update.current_status = get_child_xml(content,"current-status")
        return update

    def __str__(self):
        return "%s %s"%(self.person_name.encode('utf8'), self.current_status.encode('utf8'))

class VIRL(object):
    """
    Viral updates include comments and likes.
    """
    def __init__(self):
        self.person_name = None
        self.person_id = None
        self.person_headline = None
        self.person_public_url = None
        self.action_code = None
        self.original_timestamp = None
        self.original_update_key = None
        self.original_update_type = None
        self.update_person_id = None
        self.update_person_name = None
        self.update_person_headline = None
        self.update_share_id = None
        self.update_share_timestamp = None
        self.update_share_visibility_code = None
        self.update_share_comment = None
        self.update_share_service_provider_name = None
        self.update_share_author_id = None
        self.update_share_author_name = None
        self.update_share_author_headline = None
        self.update_person_picture_url = None
        self.update_person_public_url = None

    @staticmethod
    def create(xml_element):
        person = xml_element.find("person")
        update = VIRL()
        update.person_name = "%s %s"%(person.find("first-name").text,person.find("last-name").text)
        update.person_id = "%s"%person.find("id").text
        update.person_public_url = "%s"%person.find("site-standard-profile-request").find("url").text
        update.person_headline = "%s"%person.find("headline").text
        update_action = xml_element.find("update-action")
        update.action_code = update_action.find("action").find("code").text
        original_update = update_action.find("original-update")
        update.original_timestamp = original_update.find("timestamp").text
        update.original_update_key = original_update.find("update-key").text
        update.original_update_type = original_update.find("update-type").text
        update_person = original_update.find("update_content").find("person")
        update.update_person_id = update_person.find("id").text
        update.update_person_name = "%s %s"%(update_person.find("first-name").text,update_person.find("last-name").text)
        update.update_person_headline = "%s"%update_person.find("headline").text
        update_share = update_person.find("current-share")
        update.update_share_id = update_share.find("id").text
        update.update_share_timestamp = update_share.find("timestamp").text
        update.update_share_visibility_code = update_share.find("visibility").find("code").text
        update.update_share_comment = update_share.find("comment").text
        update.update_share_service_provider_name = update_share.find("source").find("service-provider").find("name").text
        update_share_author = update_share.find("author")
        update.update_share_author_id = update_share_author.find("id").text
        update.update_share_author_name = "%s %s"%(update_share_author.find("first-name").text,update_share_author.find("last-name").text)
        update.update_share_author_headline = update_share_author.find("headline")
        update.update_person_picture_url = person.find("picture_url").text
        update.update_person_public_url = person.find("site-standard-profile-request").find("url").text
        return update

    def __str__(self):
        return "VIRL update"


class JGRP(object):
    """
    Join group update. This update notifies that a user has joined a group.
    """
    def __init__(self):
        self.person_name = None
        self.person_id = None
        self.person_public_url = None
        self.person_headline = None

    @staticmethod
    def create(xml_element):
        update = JGRP()
        person = xml_element.find("person")
        update = create_person_attrs(update,person)
        #TODO: NOT FINISHED
        return update

#TODO: PROF, QSTN, ANSW, APPM, APPS, PICU, PRFU, PRFX, PREC, SVPR, JOBP, CMPY, MSFC

class Update(object):
    def __init__(self):
        self.timestamp = None
        self.is_commentable = None
        self.is_likeable = None
        self.is_liked = None
        self.update_type = None
        self.update_key = None
        self.num_likes = None
        self.update = None

    @staticmethod
    def create(xml_element,update_type):
        update = Update()
        update.update_type = update_type
        update.update_key = get_child_xml(xml_element,"update-key")
        update.timestamp = int(get_child_xml(xml_element,"timestamp"))
        update.is_commentable = str_to_bool(get_child_xml(xml_element,"is-commentable"))
        update.is_likeable = str_to_bool(get_child_xml(xml_element,"is-likeable"))
        update.is_liked = str_to_bool(get_child_xml(xml_element,"is-liked"))
        update.num_likes = get_child_xml(xml_element,"num-likes")
        content = xml_element.find("update-content")
        up = globals().get(update_type,None)
        if up is not None:
            update.update = up.create(content)
        return update

    def get_source(self):
        if self.update_type == "CONN":
            return self.update.person1_id,self.update.person1_name
        elif self.update_type in ("NCONN","CCEM","STAT","VIRL"):
            return self.update.person_id,self.update.person_name
        elif self.update_type == "SHAR":
            return self.update.sharer_id,self.update.sharer_name
        # this is a special case for update_types that are not yet implemented
        return self.update_type,self.update_type

    def message(self):
        return str(self.update)


