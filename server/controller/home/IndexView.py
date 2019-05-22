#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.app import db
from server.controller.home import CommonView
from flask import session

from server.models.ArticleModel import Article, ArticleCategory
from server.models.CommonModel import BannerCfg
from server.models.News import Customer, ArticleCollet


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


        return {
            "article": article,
            "author": author,
            "author_article_num": author_article_num,
            "collet_num": collet_num
        }