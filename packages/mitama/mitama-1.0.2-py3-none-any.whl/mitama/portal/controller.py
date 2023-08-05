from mitama.app import Controller, AppRegistry
from mitama.http import Response
from mitama.nodes import User, Group
from mitama.auth import password_hash, password_auth, get_jwt, AuthorizationError
from mitama.app.noimage import load_noimage_group, load_noimage_user
import json
import traceback
from uuid import uuid4
from .model import Invite, CreateUserPermission, UpdateUserPermission, DeleteUserPermission, CreateGroupPermission, UpdateGroupPermission, DeleteGroupPermission, Admin

class SessionController(Controller):
    async def login(self, request):
        template = self.view.get_template('login.html')
        if request.method == 'POST':
            try:
                post = await request.post()
                result = password_auth(post['screen_name'], post['password'])
                sess = await request.session()
                sess['jwt_token'] = get_jwt(result)
                redirect_to = request.query.get('redirect_to', '/')
                return Response.redirect(
                    redirect_to
                )
            except AuthorizationError as err:
                error = 'パスワード、またはログイン名が間違っています'
                return await Response.render(
                    template,
                    request,
                    {
                        'error':error
                    },
                    status = 401
                )
        return await Response.render(
            template,
            request,
            status = 401
        )

    async def logout(self, request):
        sess = await request.session()
        sess['jwt_token'] = None
        redirect_to = request.query.get('redirect_to', '/')
        return Response.redirect(redirect_to)

class RegisterController(Controller):
    async def signup(self, request):
        sess = await request.session()
        template = self.view.get_template('signup.html')
        invite = Invite.query.filter(Invite.token == request.query["token"]).first()
        if request.method == "POST":
            try:
                data = await request.post()
                user = User()
                user.password = password_hash(data['password'])
                if invite.editable:
                    user.screen_name = data['screen_name']
                    user.name = data['name']
                    user.icon = data['icon'].file.read() if "icon" in data else invite.icon
                else:
                    user.screen_name = invite.screen_name
                    user.name = invite.name
                    user.icon = invite.icon
                user.create()
                sess["jwt_token"] = get_jwt(user)
                return Response.redirect(
                    self.app.convert_url('/')
                )
            except Exception as err:
                error = str(err)
                return await Response.render(template, request, {
                    'error': error,
                    "name": data["name"],
                    "screen_name": data["screen_name"],
                    "password": data["password"],
                    "icon": data["icon"].file.read(),
                    'editable': invite.editable
                })
        return await Response.render(template, request, {
            "icon": invite.icon,
            "name": invite.name,
            "screen_name": invite.screen_name,
            'editable': invite.editable
        })
    async def setup(self, request):
        sess = await request.session()
        template = self.app.view.get_template('setup.html')
        if request.method == 'POST':
            try:
                data = await request.post()
                user = User()
                user.screen_name = data['screen_name']
                user.name = data['name']
                user.password = password_hash(data['password'])
                user.icon = data["icon"].file.read() if 'icon' in data else load_noimage_user()
                user.create()
                Admin.accept(user)
                CreateUserPermission.accept(user)
                UpdateUserPermission.accept(user)
                DeleteUserPermission.accept(user)
                CreateGroupPermission.accept(user)
                UpdateGroupPermission.accept(user)
                DeleteGroupPermission.accept(user)
                UpdateUserPermission.accept(user, user)
                sess["jwt_token"] = get_jwt(user)
                return Response.redirect(
                    self.app.convert_url("/")
                )
            except Exception as err:
                error = str(err)
                return await Response.render(template, request, {
                    'error': error
                })
        return await Response.render(template, request)
# HomeControllerではユーザー定義のダッシュボード的なのを作れるようにしたいけど、時間的にパス
'''
class HomeController(Controller):
    async def handle(self, request):
        template = self.view.get_template('home.html')
        return await Response.render(template, request)
'''

class UsersController(Controller):
    async def create(self, req):
        if CreateUserPermission.is_forbidden(req.user):
            return await self.app.error(req, 403)
        template = self.view.get_template('user/create.html')
        invites = Invite.list()
        if req.method == 'POST':
            post = await req.post()
            try:
                icon = post["icon"].file.read() if "icon" in post else load_noimage_user()
                invite = Invite()
                invite.name = post['name']
                invite.screen_name = post['screen_name']
                invite.icon = icon
                invite.token = str(uuid4())
                invite.editable = 'editable' in post
                invite.create()
                invites = Invites.list()
                return await Response.render(template, req, {
                    'invites': invites,
                    "icon": load_noimage_user()
                })
            except Exception as err:
                error = str(err)
                return await Response.render(template, req, {
                    'invites': invites,
                    "name": post["name"],
                    "screen_name": post["screen_name"],
                    "icon": icon,
                    'error': error
                })
        return await Response.render(template, req, {
            'invites': invites,
            "icon": load_noimage_user()
        })
    async def cancel(self, req):
        if CreateUserPermission.is_forbidden(req.user):
            return await self.app.error(req, 403)
        invite = Invite.retrieve(req.params['id'])
        invite.delete()
        return Response.redirect(self.app.convert_url('/users/invite'))
    async def retrieve(self, req):
        template = self.view.get_template('user/retrieve.html')
        user = User.retrieve(screen_name = req.params["id"])
        return await Response.render(template, req, {
            "user": user,
            'updatable': UpdateUserPermission.is_accepted(req.user, user)
        })
    async def update(self, req):
        template = self.view.get_template('user/update.html')
        user = User.retrieve(screen_name = req.params["id"])
        if UpdateUserPermission.is_forbidden(req.user, user):
            return await self.app.error(req, 403)
        if req.method == "POST":
            post = await req.post()
            try:
                icon = post["icon"].file.read() if "icon" in post else user.icon
                user.screen_name = post["screen_name"]
                user.name = post["name"]
                user.icon = icon
                user.update()
                if Admin.is_accepted(req.user):
                    if 'user_create' in post:
                        CreateUserPermission.accept(user)
                    else:
                        CreateUserPermission.forbit(user)
                    if 'user_update' in post:
                        UpdateUserPermission.accept(user)
                    else:
                        UpdateUserPermission.forbit(user)
                    if 'user_delete' in post:
                        DeleteUserPermission.accept(user)
                    else:
                        DeleteUserPermission.forbit(user)
                    if 'group_create' in post:
                        CreateGroupPermission.accept(user)
                    else:
                        CreateGroupPermission.forbit(user)
                    if 'group_update' in post:
                        UpdateGroupPermission.accept(user)
                    else:
                        UpdateGroupPermission.forbit(user)
                    if 'group_delete' in post:
                        DeleteGroupPermission.accept(user)
                    else:
                        DeleteGroupPermission.forbit(user)
                    if 'admin' in post:
                        Admin.accept(user)
                    else:
                        Admin.forbit(user)
                return await Response.render(template, req, {
                    "message": "変更を保存しました",
                    "user": user,
                    "screen_name": user.screen_name,
                    "name": user.name,
                    "icon": user.icon,
                })
            except Exception as err:
                error = str(err)
                return await Response.render(template, req, {
                    "error": error,
                    "user": user,
                    "screen_name": post["screen_name"],
                    "name": post["name"],
                    "icon": icon,
                })
        return await Response.render(template, req, {
            "user": user,
            "screen_name": user.screen_name,
            "name": user.name,
            "icon": user.icon,
        })
    async def delete(self, req):
        if DeleteUserPermission.is_forbidden(req.user):
            return await self.app.error(req, 403)
        template = self.view.get_template('user/delete.html')
        return await Response.render(template, req)
    async def list(self, req):
        template = self.view.get_template('user/list.html')
        users = User.list()
        return await Response.render(template, req, {
            'users': users,
            'create_permission': CreateUserPermission.is_accepted(req.user),
        })

class GroupsController(Controller):
    async def create(self, req):
        if CreateGroupPermission.is_forbidden(req.user):
            return await self.app.error(request, 403)
        template = self.view.get_template('group/create.html')
        groups = Group.list()
        if req.method == 'POST':
            post = await req.post()
            try:
                group = Group()
                group.name = post['name']
                group.screen_name = post['screen_name']
                group.icon = post['icon'].file.read() if "icon" in post else None
                group.create()
                if "parent" in post and post['parent'] != '':
                    Group.retrieve(int(post['parent'])).append(group)
                group.append(req.user)
                UpdateGroupPermission.accept(req.user, group)
                return Response.redirect(self.app.convert_url("/groups"))
            except Exception as err:
                error = str(err)
                return await Response.render(template, req, {
                    'groups': groups,
                    "icon": post["icon"].file.read() if "icon" in post else None,
                    'error': error
                })
        return await Response.render(template, req, {
            'groups': groups,
            "icon": load_noimage_group()
        })
    async def retrieve(self, req):
        template = self.view.get_template('group/retrieve.html')
        group = Group.retrieve(screen_name = req.params["id"])
        return await Response.render(template, req, {
            "group": group,
            'updatable': UpdateGroupPermission.is_accepted(req.user, group)
        })
    async def update(self, req):
        template = self.view.get_template('group/update.html')
        group = Group.retrieve(screen_name = req.params["id"])
        groups = list()
        for g in Group.list():
            if not (group.is_ancestor(g) or group.is_descendant(g) or g==group):
                groups.append(g)
        users = list()
        for u in User.list():
            if not group.is_in(u):
                users.append(u)
        if UpdateGroupPermission.is_forbidden(req.user, group):
            return await self.app.error(req, 403)
        if req.method == "POST":
            post = await req.post()
            try:
                print(post)
                icon = post["icon"].file.read() if "icon" in post else group.icon
                group.screen_name = post["screen_name"]
                group.name = post["name"]
                group.icon = icon
                group.update()
                if Admin.is_accepted(req.user):
                    if 'user_create' in post:
                        CreateUserPermission.accept(group)
                    else:
                        CreateUserPermission.forbit(group)
                    if 'user_update' in post:
                        UpdateUserPermission.accept(group)
                    else:
                        UpdateUserPermission.forbit(group)
                    if 'user_delete' in post:
                        DeleteUserPermission.accept(group)
                    else:
                        DeleteUserPermission.forbit(group)
                    if 'group_create' in post:
                        CreateGroupPermission.accept(group)
                    else:
                        CreateGroupPermission.forbit(group)
                    if 'group_update' in post:
                        UpdateGroupPermission.accept(group)
                    else:
                        UpdateGroupPermission.forbit(group)
                    if 'group_delete' in post:
                        DeleteGroupPermission.accept(group)
                    else:
                        DeleteGroupPermission.forbit(group)
                    if 'admin' in post:
                        Admin.accept(group)
                    else:
                        Admin.forbit(group)
                return await Response.render(template, req, {
                    "message": "変更を保存しました",
                    "group": group,
                    "screen_name": group.screen_name,
                    "name": group.name,
                    'all_groups': groups,
                    'all_users': users,
                    "icon": group.icon,
                })
            except Exception as err:
                error = str(err)
                return await Response.render(template, req, {
                    "error": error,
                    'all_groups': groups,
                    'all_users': users,
                    "group": group,
                    "screen_name": post["screen_name"],
                    "name": post["name"],
                    "icon": icon,
                })
        return await Response.render(template, req, {
            "group": group,
            'all_groups': groups,
            'all_users': users,
            "screen_name": group.screen_name,
            "name": group.name,
            "icon": group.icon,
        })
    async def append(self, req):
        post = await req.post()
        try:
            group = Group.retrieve(screen_name = req.params['id'])
            nodes = list()
            if 'user' in post:
                for uid in post['user']:
                    try:
                        nodes.append(User.retrieve(int(uid)))
                    except Exception as err:
                        pass
            if 'group' in post:
                for gid in post['group']:
                    try:
                        nodes.append(Group.retrieve(int(gid)))
                    except Exception as err:
                        pass
            group.append_all(nodes)
        except Exception as err:
            pass
        finally:
            return Response.redirect(self.app.convert_url('/groups/'+group.screen_name+'/settings'))
    async def remove(self, req):
        try:
            group = Group.retrieve(screen_name = req.params['id'])
            cid = int(req.params['cid'])
            if cid % 2 == 0:
                child = Group.retrieve(cid / 2)
            else:
                child = User.retrieve((cid + 1) / 2)
            group.remove(child)
        except Exception as err:
            pass
        finally:
            return Response.redirect(self.app.convert_url('/groups/'+group.screen_name+'/settings'))
    async def accept(self, req):
        group = Group.retrieve(screen_name = req.params['id'])
        if UpdateGroupPermission.is_forbidden(req.user, group):
            return await self.app.error(req, 403)
        user = User.retrieve(int(req.params['cid']))
        UpdateGroupPermission.accept(user, group)
        return Response.redirect(self.app.convert_url('/groups/'+group.screen_name+'/settings'))
    async def forbit(self, req):
        group = Group.retrieve(screen_name = req.params['id'])
        if UpdateGroupPermission.is_forbidden(req.user, group):
            return await self.app.error(req, 403)
        user = User.retrieve(int(req.params['cid']))
        UpdateGroupPermission.forbit(user, group)
        return Response.redirect(self.app.convert_url('/groups/'+group.screen_name+'/settings'))
    async def delete(self, req):
        if DeleteGroupPermission.is_forbidden(req.user):
            return await self.app.error(req, 403)
        template = self.view.get_template('group/delete.html')
        return await Response.render(template, req)
    async def list(self, req):
        template = self.view.get_template('group/list.html')
        groups = Group.tree()
        return await Response.render(template, req, {
            'groups': groups,
            'create_permission': CreateGroupPermission.is_accepted(req.user),
        })

class AppsController(Controller):
    async def update(self, req):
        if Admin.is_forbidden(req.user):
            return await self.app.error(req, 403)
        template = self.view.get_template('apps/update.html')
        apps = AppRegistry()
        if req.method == "POST":
            apps.reset()
            post = await req.post()
            try:
                prefix = post["prefix"]
                data = dict()
                data["apps"] = dict()
                for package, path in prefix.items():
                    data["apps"][package] = {
                        "path": path
                    }
                with open(self.app.project_root_dir / "mitama.json", 'w') as f:
                    f.write(json.dumps(data))
                apps.load_config()
                return await Response.render(template, req, {
                    'message': '変更を保存しました',
                    "apps": apps,
                })
            except Exception as err:
                return await Response.render(template, req, {
                    "apps": apps,
                    'error': str(err)
                })
        return await Response.render(template, req, {
            "apps": apps
        })
    async def list(self, req):
        template = self.view.get_template('apps/list.html')
        apps = AppRegistry()
        return await Response.render(template, req, {
            "apps": apps,
        })
