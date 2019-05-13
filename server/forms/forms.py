# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from server.app import db
from server.models.Models import MenuAuth, User
from sqlalchemy import or_
from wtforms.compat import iteritems


class BaseForm(FlaskForm):
    def get_error(self):
        erros = dict((name, f.errors) for name, f in iteritems(self._fields) if f.errors)
        error_message = erros.values()[0][0]
        return error_message


class LoginForm(BaseForm):
    username = StringField(u'用户名', validators=[DataRequired(message=u"用户名不能为空")])
    password = PasswordField(u'密码', validators=[DataRequired(message=u"密码不能为空")])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')


class MenuForm(BaseForm):
    id = IntegerField('id')
    menu_name = StringField(u'menu_name', validators=[DataRequired(message=u"菜单名称不能为空")])
    type = StringField(u'type', validators=[DataRequired(message=u"请选择菜单类型")])
    method = StringField(u'method', validators=[DataRequired(message=u"菜单地址不能为空")])
    icon = StringField(u'icon')
    is_show = StringField(u'is_show')
    parent_id = StringField(u'parent_id', validators=[DataRequired(message=u"父级id不能为空")])
    sort = IntegerField(u'sort', validators=[DataRequired(message=u"排序不能为空")])

    def validate_method(self, field):
        if (self.id.data is not None):
            # 编辑
            menu = db.session.query(MenuAuth) \
                .filter(MenuAuth.id != self.id.data) \
                .filter(MenuAuth.parent_id == self.parent_id.data,
                        or_(MenuAuth.method == self.method.data, MenuAuth.name == self.menu_name.data)).scalar()
            if menu is not None:
                raise ValidationError(u"同级菜单下，菜单名和方法不能相同")
        else:
            menu = db.session.query(MenuAuth) \
                .filter(MenuAuth.parent_id == self.parent_id.data,
                        or_(MenuAuth.method == self.method.data, MenuAuth.name == self.menu_name.data)).scalar()
            if menu is not None:
                raise ValidationError(u"同级菜单下，菜单名和方法不能相同")


class UserForm(BaseForm):
    id = IntegerField('id')
    username = StringField(u'username', validators=[DataRequired(message=u"用户名不能为空")])
    password = StringField(u'password')
    confirm_password = StringField(u'confirm_password')
    # password = StringField(u'password', validators=[DataRequired(message=u"密码不能为空")])
    # confirm_password = StringField(u'confirm_password', validators=[DataRequired(message=u"确认密码不能为空"),EqualTo('password',u'确认密码不一致')])
    email = StringField(u'email', validators=[DataRequired(message=u"邮箱不能为空"), Email(message=u"邮箱格式不正确")])
    group_id = StringField(u'group_id', validators=[DataRequired(message=u"请选择用户分组")])

    def validate_username(self, field):
        if (self.id.data is None):
            user = db.session.query(User) \
                .filter(User.username == self.username.data).scalar()
            if user is not None:
                raise ValidationError(u"当前用户名已存在")
        else:
            user = db.session.query(User) \
                .filter(User.id != self.id.data, User.username == self.username.data).scalar()
            if user is not None:
                raise ValidationError(u"当前用户名已存在")

    def validate_email(self, field):
        if (self.id.data is not None):
            user = db.session.query(User) \
                .filter(User.id != self.id.data, User.email == self.email.data).scalar()
            if user is not None:
                raise ValidationError(u"当前邮箱已存在")
        else:
            user = db.session.query(User) \
                .filter(User.email == self.email.data).scalar()
            if user is not None:
                raise ValidationError(u"当前邮箱已存在")

    def validate_password(self, field):
        if (self.id.data is not None):
            if self.password.data != self.confirm_password.data:
                raise ValidationError(u"确认密码不一致")
        else:
            if not self.password.data:
                raise ValidationError(u"密码不能为空")
            if not self.confirm_password.data:
                raise ValidationError(u"确认密码不能为空")
            if self.password.data != self.confirm_password.data:
                raise ValidationError(u"确认密码不一致")


class ErrorForm(BaseForm):
    """
    错误表单
    """
    error_code = StringField('error_code')
    error_title = StringField('error_title')
    error_content = StringField('error_content')
