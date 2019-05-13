# -*- coding:utf-8 -*-
from server.app import db
from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column


# 文章表
class Article(db.Model):
    __tablename__ = 't_article'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, doc=u"文章分类id")
    title = db.Column(db.String(128), doc=u'文章标题', nullable=False)
    cover_pic = db.Column(db.String(128), doc=u'文章封面图')
    author_id = db.Column(db.Integer, doc=u"作者id")
    content = db.Column(db.Text, doc=u"文章正文")
    description = db.Column(db.Text, doc=u"文章摘要")
    is_top = db.Column(db.Integer, doc=u"是否置顶 0不置顶 1置顶", default=0)
    is_hot = db.Column(db.Integer, doc=u"是否热门 0非热门 1热门", default=0)
    view_num = db.Column(db.Integer, doc=u"浏览量", default=0)
    source = db.Column(db.String(32), doc=u"来源", default=0)
    source_site = db.Column(db.String(32), doc=u"来源地址", default=0)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    # 添加或编辑文章
    def merge_article(self, article_dict, article_id=None):
        if article_id:
            self.id = article_id
        self.title = article_dict['title']
        self.cover_pic = article_dict['cover_pic']
        self.content = article_dict['content']
        self.author_id = article_dict['author_id']
        self.is_top = article_dict['is_top']
        db.session.merge(self)
        db.session.commit()
        return self.id

    @classmethod
    def get_article(cls, article_id):
        article = db.session.query(Article).filter(
            Article.id == article_id
        ).first()
        return article


# 文章分类表
class ArticleCategory(db.Model):
    __tablename__ = 't_article_category'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, doc=u"父级id", default=0)
    name = db.Column(db.String(32), doc=u'分类名称', nullable=False)
    cover_pic = db.Column(db.String(128), doc=u'分类图标')
    description = db.Column(db.String(128), doc=u"分类描述")
    sort = db.Column(db.Integer, doc=u"排序", default=0)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "description": self.description,
            "sort": self.sort
        }

    # 添加或编辑分类
    def merge_article_category(self, article_category_dict, article_category_id=None):
        if article_category_id:
            self.id = article_category_id
        self.name = article_category_dict['name']
        self.cover_pic = article_category_dict['cover_pic']
        self.description = article_category_dict['description']
        self.sort = article_category_dict['sort']
        db.session.merge(self)
        db.session.commit()
        return self.id

    @classmethod
    def get_category_all(cls):
        categorys = db.session.query(ArticleCategory).order_by(ArticleCategory.sort.desc()).all()
        return categorys

    @classmethod
    def get_category(cls, cid):
        category = db.session.query(ArticleCategory).filter(ArticleCategory.id == cid).first()
        return category


# 文章评论表
class ArticleComment(db.Model):
    __tablename__ = 't_article_comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, doc=u'评论内容', nullable=False)
    customer_id = db.Column(db.Integer, doc=u'用户id', nullable=False)
    article_id = db.Column(db.Integer, doc=u'文章id', nullable=False)
    laud_no = db.Column(db.Integer, doc=u"点赞数量")
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    # 添加或编辑评论
    def merge_article_comment(self, article_id, content, customer_id, comment_id=None):
        if comment_id:
            self.id = comment_id
        self.article_id = article_id
        self.content = content
        self.customer_id = customer_id
        db.session.merge(self)
        db.session.commit()
        return self.id

        # 文章关键词


class ArticleKeywords(db.Model):
    __tablename__ = 't_article_keywords'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), doc=u'关键词', nullable=False)
    font_color = db.Column(db.String(20), doc=u'字体颜色', default='#000000', nullable=False)
    background_color = db.Column(db.String(20), doc=u'字体颜色', default='#000000', nullable=False)
    border_color = db.Column(db.String(20), doc=u'边框颜色', default='#000000', nullable=False)
    hot_no = db.Column(db.Integer, doc=u"热门搜索次数", default=0)
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "font_color": self.font_color,
            "background_color": self.background_color,
            "border_color": self.border_color,
            "hot_no": self.hot_no
        }

    # 添加或编辑文章关键词
    def merge_keywords(self, keyword_dict, keyword_id=None):
        if keyword_id:
            self.id = keyword_id
        self.name = keyword_dict['name']
        self.font_color = keyword_dict['font_color']
        self.background_color = keyword_dict['background_color']
        self.border_color = keyword_dict['border_color']
        db.session.merge(self)
        db.session.commit()
        return self.id


# 文章分类关联表
class ArticleKeywordRelation(db.Model):
    __tablename__ = 't_article_keyword_relation'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, doc=u'文章id', nullable=False)
    keyword_id = db.Column(db.Integer, doc=u'文章关键词id', nullable=False)

    @classmethod
    def get_keyword_ids(cls, article_id):
        keyword_ids = db.session.query(ArticleKeywordRelation.keyword_id).filter(
            ArticleKeywordRelation.article_id == article_id
        ).all()
        ids = []
        for keyword in keyword_ids:
            ids.append(str(keyword.keyword_id))
        return ids

    @classmethod
    def del_keyword(cls, article_id):
        db.session.query(ArticleKeywordRelation).filter(
            ArticleKeywordRelation.article_id == article_id
        ).delete()
