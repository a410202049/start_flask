#!/usr/bin/python
# -*- encoding: utf-8 -*-

from server.app import db
from server.controller.home import CommonView
from server.exception import BusinessException, PASSWORD_NOT_MATCH
from server.model.TestModel import Teacher, Student


class HomeBase(CommonView):

    def dispatch_request(self):
        context = {"school": {"name": u"北京大学"}}
        context.update(self.render_data())
        return self.render_template(context)


class HomeIndex(HomeBase):

    def render_data(self):
        # data = db.session.query(Teacher).all()
        # data1 = db.session.query(Teacher).first()
        # data2 = db.session.query(Teacher).filter(
        #     Teacher.mobile == '15208491442',
        #     Teacher.id == '2'
        # ).first()
        # data3 = db.session.query(Teacher).filter(
        #     Teacher.id == '1'
        # ).scalar()
        #
        # ret = db.session.query(Teacher).filter(
        #     Teacher.id == '1'
        # ).update(
        #     {
        #         Teacher.name: "test123"
        #     }
        # )

        # ret = db.session.query(Teacher).filter(
        #     Teacher.id == '1'
        # ).first()
        # ret.name = 'test_456'
        # ret.mobile = '15208491440'
        # db.session.merge(ret)

        # teacher = Teacher()
        # # teacher.serial_no = '123456'
        # teacher.name = u'新增老师'
        # teacher.mobile = '110'
        # db.session.add(teacher)
        # db.session.commit()

        data4 = db.session.query(
            Student
        ).join(
            Teacher, Student.teacher_id == Teacher.id
        ).filter(
            Teacher.id == '2'
        ).all()

        print data4

        # outerjoin

        # a = db.session.query(Teacher).filter(
        #     Teacher.id == '7'
        # ).delete()

        db.session.commit()
        # db.session.rollback()

        # print db.session.limit(1).all()  # 最多返回 1 条记录
        # print db.session.offset(1).all()  # 从第 2 条记录开始返回

        # print data1
        self.logger.info(u'这是测试日志')
        # return {"student": {"name": "kerry"}}

        if 1 != 2:
            raise BusinessException(u'密码不正确', PASSWORD_NOT_MATCH)



# class UserAPI(MethodView):
#     # decorators = [home_login_required]
#
#     def get(self, user_id):
#         return json.jsonify({"a": user_id})
#
#     def post(self, user_id):
#         return json.jsonify({"b": user_id})
