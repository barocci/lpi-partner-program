#
# -*- coding: utf-8
# vim: set fileencoding=utf-8

from django.contrib import admin
from redmine.models import *

class TokenAdmin(admin.ModelAdmin):
    list_display = ('value', 'action', 'user', 'created_on')
    list_filter = ('action', 'created_on')
    search_fields = ['value']
admin.site.register(Token, TokenAdmin)

class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'hide_mail', 'time_zone')
    list_filter = ('hide_mail', 'time_zone')
    search_fields = ['value', 'others']
admin.site.register(UserPreference, UserPreferenceAdmin)

class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('tracker', 'role', 'old_status', 'new_status',)
    list_filter = ('role', 'tracker', 'old_status', 'new_status',)
admin.site.register(Workflow, WorkflowAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'assignable', 'builtin', 'issues_visibility')
    list_filter = ('position', 'assignable', 'builtin', 'issues_visibility')
admin.site.register(Role, RoleAdmin)

class VersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'project', 'status', 'sharing', 'effective_date',)
    list_filter = ('status', 'sharing', 'effective_date', 'project', )
    list_display_links =('name', 'description', )
admin.site.register(Version, VersionAdmin)

class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'author', 'created_on',)
    list_filter = ('created_on', 'project', )
admin.site.register(New, NewAdmin)

class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'assigned_to', )
    list_filter = ('project', )
    search_fields = ['name']
admin.site.register(IssueCategory, IssueCategoryAdmin)

class CustomValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'customized_type', 'custom_field', 'customized_id')
    list_filter = ('customized_type', 'custom_field', )
    search_fields = ['value']
admin.site.register(CustomValue, CustomValueAdmin)

class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('url', 'project','type')
    list_filter = ('type', )
admin.site.register(Repository, RepositoryAdmin)

class JournalAdmin(admin.ModelAdmin):
    list_display = ('journalized_type', 'journalized_id', 'user', 'created_on')
    list_filter = ('created_on', 'journalized_type', )
admin.site.register(Journal, JournalAdmin)

class EnumerationAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_default', 'type', 'active', 'project', 'parent',)
    list_filter = ('position', 'is_default', 'type', 'active',)
admin.site.register(Enumeration, EnumerationAdmin)

class ChangeAdmin(admin.ModelAdmin):
    list_display = ('path', 'action', 'changeset', )
    list_filter = ('action', )
admin.site.register(Change, ChangeAdmin)

class EnabledModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', )
    list_filter = ('name', 'project',)
admin.site.register(EnabledModule, EnabledModuleAdmin)

class WatcherAdmin(admin.ModelAdmin):
    list_display = ('user', 'watchable_type', 'watchable_id')
    list_filter = ('watchable_type',)
admin.site.register(Watcher, WatcherAdmin)

class WikiPageAdmin(admin.ModelAdmin):
    list_display = ('wiki', 'title', 'protected', 'created_on')
    list_filter = ('protected', 'created_on', 'wiki',)
    list_display_links =('title', )
admin.site.register(WikiPage, WikiPageAdmin)

class WikiContentAdmin(admin.ModelAdmin):
    list_display = ('page', 'author', 'updated_on', 'version')
    list_filter = ('updated_on', )
    search_fields = ['page__title', 'text']
admin.site.register(WikiContent, WikiContentAdmin)

class WikiContentVersionAdmin(admin.ModelAdmin):
    list_display = ('page', 'author', 'updated_on', 'version')
    list_filter = ( 'updated_on',)
    search_fields = ['page__title', 'data']
admin.site.register(WikiContentVersion, WikiContentVersionAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'homepage', 'status', 'parent', 'identifier', 'is_public', )
    list_filter = ('status', 'is_public', )
    search_fields = ['name', 'homepage', 'idendifier']
admin.site.register(Project,ProjectAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('board', 'subject', 'author', 'locked', 'sticky', )
    list_filter = ('locked', 'sticky', )
admin.site.register(Message, MessageAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'firstname', 'lastname', 'mail', 'last_login_on', 'admin', 'status')
    list_filter = ('status', 'admin', 'mail_notification',)
admin.site.register(User, UserAdmin)

class GroupUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(GroupUser, GroupUserAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'mail_notification', 'created_on', )
    list_filter = ('mail_notification', 'created_on', )
admin.site.register(Member, MemberAdmin)

class MemberRoleAdmin(admin.ModelAdmin):
    list_display = ("member", "role", "inherited_from",)
    list_filter = ("role",)
    raw_id_fields = ("member",)
admin.site.register(MemberRole, MemberRoleAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = ('subject', 'tracker', 'project', 'author', 'assigned_to', 'status', 'priority', )
    list_filter = ('updated_on', 'status', 'tracker',)
admin.site.register(Issue, IssueAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'filesize', 'content_type', 'author', 'created_on', 'downloads', )
    list_filter = ('created_on', 'content_type', )
admin.site.register(Attachment, AttachmentAdmin)

class WikiAdmin(admin.ModelAdmin):
    list_display = ('project', 'start_page', 'status', )
    list_filter = ('status', )
admin.site.register(Wiki, WikiAdmin)

class ChangesetAdmin(admin.ModelAdmin):
    list_display = ('revision', 'repository', 'committer', 'committed_on', )
    list_filter = ('committed_on', 'repository',)
admin.site.register(Changeset, ChangesetAdmin)

class IssueStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_closed', 'is_default', )
    list_filter = ('position', 'is_closed', 'is_default', )
admin.site.register(IssueStatus, IssueStatusAdmin)

class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'field_format', 'is_required', 'is_for_all', 'is_filter', )
    list_filter = ('type', 'field_format', 'is_required', 'is_for_all', 'is_filter',)
admin.site.register(CustomField, CustomFieldAdmin)

class BoardAdmin(admin.ModelAdmin):
    list_display = ("project", "name", "position", "topics_count", "messages_count")
    list_filter = ("position", "project", )
admin.site.register(Board, BoardAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "commented_type", "commented_id", "created_on", "updated_on", )
    list_filter = ("commented_type", "updated_on", )
admin.site.register(Comment, CommentAdmin)

class DocumentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Document, DocumentAdmin)

class IssueRelationAdmin(admin.ModelAdmin):
    list_display = ('issue_from', 'relation_type', 'issue_to', 'delay', )
    list_filter = ('relation_type', 'delay',)
    list_display_links = ('relation_type', )
admin.site.register(IssueRelation, IssueRelationAdmin)

class JournalDetailAdmin(admin.ModelAdmin):
    list_display = ('journal', 'property')
    list_filter = ('property',)
admin.site.register(JournalDetail, JournalDetailAdmin)

class QueryAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'user', 'is_public',)
    list_filter = ('is_public', )
admin.site.register(Query, QueryAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_on')
admin.site.register(Setting, SettingAdmin)

class TimeEntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(TimeEntry, TimeEntryAdmin)

class TrackerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_in_chlog', 'is_in_roadmap',)
    list_filter = ('is_in_chlog', 'is_in_roadmap',)
    ordering = ('position', )
admin.site.register(Tracker, TrackerAdmin)

class WikiRedirectAdmin(admin.ModelAdmin):
    pass
admin.site.register(WikiRedirect, WikiRedirectAdmin)

# vim: ai ts=4 sts=4 et sw=4

