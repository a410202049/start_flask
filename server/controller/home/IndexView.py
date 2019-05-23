#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.app import db
from server.controller.home import CommonView
from flask import session

from server.models.ArticleModel import Article, ArticleCategory
from server.models.CommonModel import BannerCfg
from server.models.News import Customer, ArticleCollet, ArticleComment


class HomeBase(CommonView):

    def dispatch_request(self, *args, **kwargs):
        current_user = session.get('current_user')
        context = {}
        if current_user:
            uid = current_user['uid']
            user_info = db.session.query(Customer).filter(
                Customer.id == uid
            ).first()
            context['user_info'] = user_info

        context.update(self.render_data(*args, **kwargs))
        return self.render_template(context)


class HomeIndex(HomeBase):

    def render_data(self):
        banners = db.session.query(
            BannerCfg
        ).order_by(BannerCfg.sort.desc()).all()

        new_articles = db.session.query(
            Article.id,
            Article.title,
            Article.description,
            Article.cover_pic,
            Article.create_time,
            ArticleCategory.name.label('category_name'),
            Customer.nickname,
            Customer.username

        ).join(
            ArticleCategory, ArticleCategory.id == Article.cid
        ).join(
            Customer, Customer.id == Article.author_id
        ).order_by(Article.create_time.desc()).limit(3).all()

        hot_articles = db.session.query(
            Article.id,
            Article.title,
            Article.description,
            Article.cover_pic,
            Article.create_time,
            ArticleCategory.name.label('category_name')
        ).join(
            ArticleCategory, ArticleCategory.id == Article.cid
        ).filter(
            Article.is_hot == 1
        ).order_by(Article.create_time.desc()).limit(10).all()

        top_articles = db.session.query(
            Article.id,
            Article.title,
            Article.description,
            Article.cover_pic,
            Article.create_time,
            ArticleCategory.name.label('category_name')
        ).join(
            ArticleCategory, ArticleCategory.id == Article.cid
        ).filter(
            Article.is_top == 1
        ).order_by(Article.create_time.desc()).limit(2).all()


        return {
            "banners": banners,
            "new_articles": new_articles,
            "hot_articles": hot_articles,
            "top_articles": top_articles,
        }


class ArticleDetail(HomeBase):

    def render_data(self, article_id):
        current_user = session.get('current_user', None)

        collet_status = None
        if current_user:
            uid = current_user['uid']
            collet_status = db.session.query(
                ArticleCollet
            ).filter(
                ArticleCollet.article_id == article_id,
                ArticleCollet.uid == uid
            ).count()

        article = db.session.query(
            Article
        ).filter(
            Article.id == article_id
        ).first()

        author = db.session.query(Customer).filter(
            Customer.id == article.author_id
        ).first()

        author_article_num = db.session.query(
            Article
        ).filter(
            Article.author_id == article.author_id
        ).count()

        collet_num = db.session.query(
            ArticleCollet
        ).filter(
            ArticleCollet.article_id == article.id
        ).count()


        comment_obj_list = db.session.query(
            ArticleComment, Customer
        ).join(
            Customer, ArticleComment.uid == Customer.id
        ).filter(
            ArticleComment.article_id == article_id,
            ArticleComment.comment_id == 0
        ).all()

        comment_list = []

        for comment, customer in comment_obj_list:
            reply_list = []
            comment_dict = {}
            comment_dict['comment_id'] = comment.id
            comment_dict['content'] = comment.content
            comment_dict['user_avatar'] = customer.avatar
            comment_dict['nickname'] = customer.nickname
            comment_dict['create_time'] = comment.create_time

            reply_obj_list = db.session.query(
                ArticleComment, Customer
            ).join(
                Customer, ArticleComment.uid == Customer.id
            ).filter(
                ArticleComment.comment_id == comment.id,
                ArticleComment.commten_type == 1
            ).all()

            for reply, reply_customer in reply_obj_list:
                reply_dict = {}
                reply_dict['reply_id'] = reply.id
                reply_dict['content'] = reply.content
                reply_dict['user_avatar'] = reply_customer.avatar
                reply_dict['nickname'] = reply_customer.nickname
                reply_dict['create_time'] = reply.create_time
                reply_list.append(reply_dict)

            comment_dict['reply_list'] = reply_list
            comment_list.append(comment_dict)

        resp = {
            "article": article,
            "author": author,
            "author_article_num": author_article_num,
            "collet_num": collet_num,
            "collet_status": collet_status,
            "comment_list": comment_list
        }
        return resp