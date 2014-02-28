#
# -*- coding: utf-8
# vim: set fileencoding=utf-8

from django.db import models
from django.conf import settings


if settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
    BOOLEAN_CHOICE = ( ('f', 'False'), ('t', 'True'),)
    class MyBooleanField(models.CharField):
        def __init__(self, *args):
            models.CharField.__init__(self, max_length=1, choices=BOOLEAN_CHOICE, *args)
else:
    MyBooleanField = models.BooleanField


class Comment(models.Model):
    commented_type = models.CharField(max_length=90)
    commented_id = models.IntegerField()
    author = models.ForeignKey("User")
    comments = models.TextField(blank=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    class Meta:
        db_table = u'comments'

class CustomField(models.Model):
    type = models.CharField(max_length=90)
    name = models.CharField(max_length=90)
    field_format = models.CharField(max_length=90)
    possible_values = models.TextField(blank=True)
    regexp = models.CharField(max_length=765, blank=True)
    min_length = models.IntegerField()
    max_length = models.IntegerField()
    is_required = MyBooleanField()
    is_for_all = MyBooleanField()
    is_filter = MyBooleanField()
    position = models.IntegerField(blank=True)
    searchable = MyBooleanField(blank=True)
    default_value = models.TextField(blank=True)
    editable = MyBooleanField(blank=True)
    visible= MyBooleanField()
    class Meta:
        db_table = u'custom_fields'
    def __unicode__(self):
        return self.name

class Enumeration(models.Model):
    name = models.CharField(max_length=90)
    position = models.IntegerField(null=True, blank=True)
    is_default = MyBooleanField()
    type = models.CharField(max_length=765, blank=True)
    active = MyBooleanField()
    project = models.ForeignKey("Project", null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    class Meta:
        db_table = u'enumerations'
    def __unicode__(self):
        return self.name

class IssueRelation(models.Model):
    issue_from = models.ForeignKey("Issue", related_name="related_from")
    issue_to = models.ForeignKey("Issue", related_name="related_to")
    relation_type = models.CharField(max_length=765)
    delay = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'issue_relations'
    def __unicode__(self):
        if self.delay:
            return u"%d %s %d (delay=%d)" % (self.issue_from.id, self.relation_type, self.issue_to.id, self.delay)
        else:
            return u"%d %s %d" % (self.issue_from.id, self.relation_type, self.issue_to.id)

class IssueStatus(models.Model):
    name = models.CharField(max_length=90)
    is_closed = MyBooleanField()
    is_default = MyBooleanField()
    position = models.IntegerField(null=True, blank=True)
    default_done_ratio = models.IntegerField(null=True, blank=True) # boolean ?
    class Meta:
        db_table = u'issue_statuses'
        verbose_name_plural = u'Issue statuses'
    def __unicode__(self):
        return self.name

USER_STATUS_ANONYMOUS  = 0
USER_STATUS_ACTIVE     = 1
USER_STATUS_REGISTERED = 2
USER_STATUS_LOCKED     = 3
USER_STATUS_CHOICES = (
    (USER_STATUS_ANONYMOUS, "Anonymous"),
    (USER_STATUS_ACTIVE, "Active"),
    (USER_STATUS_REGISTERED, "Registered"),
    (USER_STATUS_LOCKED, "Locked"),
)

class User(models.Model):
    login = models.CharField(max_length=90)
    hashed_password = models.CharField(max_length=120)
    firstname = models.CharField(max_length=90)
    lastname = models.CharField(max_length=90)
    mail = models.CharField(max_length=180)
    admin = MyBooleanField()
    status = models.IntegerField(choices=USER_STATUS_CHOICES)
    last_login_on = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=15, blank=True)
    auth_source_id = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=765, blank=True)
    identity_url = models.CharField(max_length=765, blank=True)
    mail_notification = models.CharField(max_length=765)
    salt = models.CharField(max_length=192, blank=True)
    class Meta:
        db_table = u'users'
    def __unicode__(self):
        return u"%s %s" % (self.firstname, self.lastname)

PROJECT_STATUS_CHOICE = ( (1, 'Active'), (9, 'Archived'),)

class Project(models.Model):
    name = models.CharField(max_length=765)
    description = models.TextField(blank=True)
    homepage = models.CharField(max_length=765, blank=True)
    is_public = MyBooleanField()
    parent = models.ForeignKey('self', null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    identifier = models.CharField(max_length=765, blank=True)
    status = models.IntegerField(choices=PROJECT_STATUS_CHOICE)
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'projects'
    def __unicode__(self):
        return self.name

class Document(models.Model):
    project= models.ForeignKey(Project)
    category_id = models.IntegerField()
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'documents'

class EnabledModule(models.Model):
    project= models.ForeignKey(Project, null=True, blank=True)
    name = models.CharField(max_length=765)
    class Meta:
        db_table = u'enabled_modules'
    def __unicode__(self):
        return self.name

class IssueCategory(models.Model):
    project= models.ForeignKey(Project)
    name = models.CharField(max_length=90)
    assigned_to = models.ForeignKey(User, null=True, blank=True)
    class Meta:
        db_table = u'issue_categories'
        verbose_name_plural = u'Issue categories'
    def __unicode__(self):
        return self.name

class New(models.Model):
    project= models.ForeignKey(Project, null=True, blank=True)
    title = models.CharField(max_length=180)
    summary = models.CharField(max_length=765, blank=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User)
    created_on = models.DateTimeField(null=True, blank=True)
    comments_count = models.IntegerField()
    class Meta:
        db_table = u'news'
    def __unicode__(self):
        return self.title

class Query(models.Model):
    project= models.ForeignKey(Project, null=True, blank=True)
    name = models.CharField(max_length=765)
    filters = models.TextField(blank=True)
    user= models.ForeignKey(User)
    is_public = MyBooleanField()
    column_names = models.TextField(blank=True)
    sort_criteria = models.TextField(blank=True)
    group_by = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'queries'
        verbose_name_plural = u'Queries'
    def __unicode__(self):
        return self.name

class Repository(models.Model):
    project= models.ForeignKey(Project)
    url = models.CharField(max_length=765)
    login = models.CharField(max_length=180, blank=True)
    password = models.CharField(max_length=765, blank=True)
    root_url = models.CharField(max_length=765, blank=True)
    type = models.CharField(max_length=765, blank=True)
    path_encoding = models.CharField(max_length=192, blank=True)
    log_encoding = models.CharField(max_length=192, blank=True)
    extra_info = models.TextField(blank=True)
    class Meta:
        db_table = u'repositories'
    def __unicode__(self):
        return self.url

ROLE_BUILTIN_NON_MEMBER = 1
ROLE_BUILTIN_ANONYMOUS = 2
ROLE_BUILTIN_CHOICES = (
    (ROLE_BUILTIN_NON_MEMBER, "Non member"),
    (ROLE_BUILTIN_ANONYMOUS, "Anonymous"),
)
class Role(models.Model):
    name = models.CharField(max_length=90)
    position = models.IntegerField(null=True, blank=True)
    assignable = MyBooleanField(blank=True)
    builtin = models.IntegerField(choices=ROLE_BUILTIN_CHOICES)
    permissions = models.TextField(blank=True)
    issues_visibility = models.CharField(max_length=90)
    class Meta:
        db_table = u'roles'
    def __unicode__(self):
        return self.name

class SchemaMigration(models.Model):
    version = models.CharField(unique=True, max_length=255) # should be 255
    class Meta:
        db_table = u'schema_migrations'

class Setting(models.Model):
    name = models.CharField(max_length=765)
    value = models.TextField(blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'settings'
    def __unicode__(self):
        return self.name

class Token(models.Model):
    user= models.ForeignKey(User)
    action = models.CharField(max_length=90)
    value = models.CharField(max_length=120)
    created_on = models.DateTimeField()
    class Meta:
        db_table = u'tokens'

class Tracker(models.Model):
    name = models.CharField(max_length=90)
    is_in_chlog = MyBooleanField()
    position = models.IntegerField(null=True, blank=True)
    is_in_roadmap = MyBooleanField()
    class Meta:
        db_table = u'trackers'
    def __unicode__(self):
        return self.name

class ProjectTracker(models.Model):
    project= models.ForeignKey(Project)
    tracker = models.ForeignKey(Tracker, unique=True)
    class Meta:
        db_table = u'projects_trackers'

class UserPreference(models.Model):
    user= models.ForeignKey(User)
    others = models.TextField(blank=True)
    hide_mail = MyBooleanField(blank=True)
    time_zone = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'user_preferences'

class Version(models.Model):
    project= models.ForeignKey(Project)
    name = models.CharField(max_length=765)
    description = models.CharField(max_length=765, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    wiki_page_title = models.CharField(max_length=765, blank=True)
    status = models.CharField(max_length=765, blank=True)
    sharing = models.CharField(max_length=765)
    class Meta:
        db_table = u'versions'
    def __unicode__(self):
        return self.name

class Watcher(models.Model):
    watchable_type = models.CharField(max_length=255)
    watchable_id = models.IntegerField()
    user= models.ForeignKey(User, null=True, blank=True)
    class Meta:
        db_table = u'watchers'
    def __unicode__(self):
        return u"%s : %s %d" % (self.user, self.watchable_type, self.watchable_id)

class Wiki(models.Model):
    project= models.ForeignKey(Project)
    start_page = models.CharField(max_length=765)
    status = models.IntegerField()
    class Meta:
        db_table = u'wikis'
    def __unicode__(self):
        return u"wiki %s" % self.project

class WikiPage(models.Model):
    wiki = models.ForeignKey(Wiki)
    title = models.CharField(max_length=765)
    created_on = models.DateTimeField()
#    protected = models.BooleanField()
    protected = MyBooleanField()
    parent = models.ForeignKey("self", null=True, blank=True)
    class Meta:
        db_table = u'wiki_pages'
    def __unicode__(self):
        return self.title

class WikiContent(models.Model):
    page = models.ForeignKey(WikiPage)
    author = models.ForeignKey(User, null=True, blank=True)
    text = models.TextField(blank=True)
    comments = models.CharField(max_length=765, blank=True)
    updated_on = models.DateTimeField()
    version = models.IntegerField()
    class Meta:
        db_table = u'wiki_contents'
    def __unicode__(self):
        return "content:%s" % self.page

class WikiContentVersion(models.Model):
    wiki_content = models.ForeignKey(WikiContent)
    page = models.ForeignKey(WikiPage)
    author = models.ForeignKey(User, null=True, blank=True)
    data = models.TextField(blank=True)
    compression = models.CharField(max_length=18, blank=True)
    comments = models.CharField(max_length=765, blank=True)
    updated_on = models.DateTimeField()
    version = models.IntegerField()
    class Meta:
        db_table = u'wiki_content_versions'
    def __unicode__(self):
        return "%s (#%d)" % (self.page, self.version)

class WikiRedirect(models.Model):
    wiki = models.ForeignKey(Wiki)
    title = models.CharField(max_length=765, blank=True)
    redirects_to = models.CharField(max_length=765, blank=True)
    created_on = models.DateTimeField()
    class Meta:
        db_table = u'wiki_redirects'
    def __unicode__(self):
        return u"%s -> %s" % (self.title, self.redirects_to)

class Workflow(models.Model):
    tracker= models.ForeignKey(Tracker)
    old_status = models.ForeignKey(IssueStatus, related_name='old')
    new_status = models.ForeignKey(IssueStatus, related_name='new')
    role = models.ForeignKey(Role)
    assignee = models.IntegerField()
    author = models.IntegerField()
    class Meta:
        db_table = u'workflows'
    def __unicode__(self):
        return u"%s/%s: %s -> %s" % (self.role, self.tracker, self.old_status, self.new_status)

class Board(models.Model):
    project= models.ForeignKey(Project)
    name = models.CharField(max_length=765)
    description = models.CharField(max_length=765, blank=True)
    position = models.IntegerField(null=True, blank=True)
    topics_count = models.IntegerField()
    messages_count = models.IntegerField()
    last_message = models.ForeignKey('Message', null=True, blank=True, related_name='last')
    class Meta:
        db_table = u'boards'
    def __unicode__(self):
        return self.name

class Message(models.Model):
    board = models.ForeignKey(Board)
    parent = models.ForeignKey('self', null=True, blank=True)
    subject = models.CharField(max_length=765)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, null=True, blank=True)
    replies_count = models.IntegerField()
    last_reply_id = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    locked = MyBooleanField(blank=True)
    sticky = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'messages'

class GroupUser(models.Model):
    group_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User", unique=True)
    class Meta:
        db_table = u'groups_users'

class MemberRole(models.Model):
    member = models.ForeignKey("Member")
    role = models.ForeignKey("Role")
    inherited_from = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'member_roles'

class Member(models.Model):
    user= models.ForeignKey(User)
    project= models.ForeignKey(Project)
#    project_id = models.IntegerField()
    created_on = models.DateTimeField(null=True, blank=True)
    mail_notification = MyBooleanField()
    class Meta:
        db_table = u'members'
    def __unicode__(self):
        return u"%s/%s" % (unicode(self.user), self.project.name)
        return u"%s/%s" % (unicode(self.user), self.project_id)

class Journal(models.Model):
    journalized_id = models.IntegerField()
    journalized_type = models.CharField(max_length=90)
    user= models.ForeignKey(User)
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField()
    class Meta:
        db_table = u'journals'
    def __unicode__(self):
        return u"id=%d type=%s" % (self.journalized_id, self.journalized_type)

class JournalDetail(models.Model):
    journal = models.ForeignKey(Journal)
    property = models.CharField(max_length=90)
    prop_key = models.CharField(max_length=90)
    old_value = models.TextField(blank=True)
    value = models.TextField(blank=True)
    class Meta:
        db_table = u'journal_details'

class Issue(models.Model):
    tracker= models.ForeignKey(Tracker)
    project= models.ForeignKey(Project)
    subject = models.CharField(max_length=765)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    category= models.ForeignKey(IssueCategory, null=True, blank=True)
    status= models.ForeignKey(IssueStatus)
    assigned_to = models.ForeignKey(User, null=True, blank=True, related_name='assigned')
    priority = models.ForeignKey(Enumeration)
    fixed_version = models.ForeignKey(Version, null=True, blank=True)
    author= models.ForeignKey(User, related_name='author')
    lock_version = models.IntegerField()
    created_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    done_ratio = models.IntegerField()
    estimated_hours = models.FloatField(null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    root_id = models.IntegerField(null=True, blank=True)
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    is_private = MyBooleanField()
    class Meta:
        db_table = u'issues'
    def __unicode__(self):
        return u"Issue #%d" % self.id

class TimeEntry(models.Model):
    project= models.ForeignKey(Project)
    user= models.ForeignKey(User)
    issue = models.ForeignKey(Issue, null=True, blank=True)
    hours = models.FloatField()
    comments = models.CharField(max_length=765, blank=True)
    activity_id = models.IntegerField()
    spent_on = models.DateField()
    tyear = models.IntegerField()
    tmonth = models.IntegerField()
    tweek = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    class Meta:
        db_table = u'time_entries'
        verbose_name_plural = u'Time entries'

class Attachment(models.Model):
    container_id = models.IntegerField()
    container_type = models.CharField(max_length=90)
    filename = models.CharField(max_length=765)
    disk_filename = models.CharField(max_length=765)
    filesize = models.IntegerField()
    content_type = models.CharField(max_length=765, blank=True)
    digest = models.CharField(max_length=120)
    downloads = models.IntegerField()
    author= models.ForeignKey(User)
    created_on = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'attachments'
    def __unicode__(self):
        return self.filename

class Changeset(models.Model):
    repository = models.ForeignKey(Repository)
    revision = models.CharField(unique=True, max_length=255) # should be 765
    committer = models.CharField(max_length=765, blank=True)
    committed_on = models.DateTimeField()
    comments = models.TextField(blank=True)
    commit_date = models.DateField(null=True, blank=True)
    scmid = models.CharField(max_length=765, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    class Meta:
        db_table = u'changesets'
    def __unicode__(self):
        return self.revision

class ChangesetsIssue(models.Model):
    changeset = models.ForeignKey(Changeset, unique=True)
    issue = models.ForeignKey(Issue, unique=True)
    class Meta:
        db_table = u'changesets_issues'

CHANGE_ACTION_CHOICES = ( ('A', 'Added'), ('M', 'Modified'), ('D', 'Delete'),)

class Change(models.Model):
    changeset = models.ForeignKey(Changeset)
    action = models.CharField(max_length=1, choices=CHANGE_ACTION_CHOICES)
    path = models.TextField()
    from_path = models.TextField(blank=True)
    from_revision = models.CharField(max_length=765, blank=True)
    revision = models.CharField(max_length=765, blank=True)
    branch = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'changes'

class CustomFieldsProject(models.Model):
    custom_field = models.ForeignKey(CustomField)
    project= models.ForeignKey(Project)
    class Meta:
        db_table = u'custom_fields_projects'

class CustomFieldsTracker(models.Model):
    custom_field = models.ForeignKey(CustomField)
    tracker = models.ForeignKey(Tracker)
    class Meta:
        db_table = u'custom_fields_trackers'

class CustomValue(models.Model):
    customized_type = models.CharField(max_length=90)
    customized_id = models.IntegerField()
    custom_field = models.ForeignKey(CustomField)
    value = models.TextField(blank=True)
    class Meta:
        db_table = u'custom_values'
    def __unicode__(self):
        return self.value

# vim: ai ts=4 sts=4 et sw=4

