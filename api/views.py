from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book, Users
from api.serializers import BookModelSerializerV2, BookModelSerializerV3, UserModelSerializer, BookModelSerializer, \
    BookDeModelSerializer


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            book = Book.objects.get(pk=book_id)

            data = BookModelSerializer(book).data

            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": data,
            })

        else:
            book_objects_all = Book.objects.all()

            book_ser = BookModelSerializer(book_objects_all, many=True).data

            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": book_ser,
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data

        serializer = BookDeModelSerializer(data=request_data)

        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()

        return Response({
            "status": 200,
            "message": "添加图书成功",
            "results": BookModelSerializer(book_obj).data,
        })


class BookAPIViewV2(APIView):

    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            book = Book.objects.get(pk=book_id, is_delete=False)

            data = BookModelSerializerV2(book).data

            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": data,
            })

        else:
            book_objects_all = Book.objects.filter(is_delete=False)

            book_ser = BookModelSerializerV2(book_objects_all, many=True).data

            return Response({
                "status": 200,
                "message": "查询单个图书成功",
                "results": book_ser,
            })

    def post(self, request, *args, **kwargs):
        """
        增加单个: 传递参数是字典
        增加多个: [{},{},{}] 列表中嵌套是一个个的图书对象
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.data

        if isinstance(request_data, dict):  # 代表添加的单个对象
            many = False
        elif isinstance(request_data, list):  # 代表添加的是多个对象
            many = True
        else:
            return Response({
                "status": 400,
                "message": "参数格式有误",
            })

        serializer = BookModelSerializerV2(data=request_data, many=many)

        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()

        return Response({
            "status": 200,
            "message": "添加图书成功",
            "results": BookModelSerializerV2(book_obj, many=many).data,
        })

    def delete(self, request, *args, **kwargs):
        """
        删除单个  删除多个
        单个删除: 通过url传递单个删除的id
        多个删除: 有多个id {ids:[1,2,3]}
        :return:
        """
        book_id = kwargs.get("id")

        if book_id:
            # 删除单个
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get("ids")

        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        print(response)
        if response:
            return Response({
                "status": 200,
                "message": '删除成功'
            })

        return Response({
            "status": 400,
            "message": '删除失败或者图书存在'
        })

    def put(self, request, *args, **kwargs):
        """
        整体修改单个:  修改一个对象的全部字段
        修改对象时,在调用序列化器验证数据时必须指定instance关键字
        在调用serializer.save() 底层是通过ModelSerializer内部的update()方法来完成的更新
        """

        # 获取要修改的对象的值
        request_data = request.data
        # 获取要修改的图书的id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 400,
                "message": '图书不存在'
            })

        # 更新的时候需要对前端传递的数据进行安全校验
        # 更新的时候需要指定关键字参数data
        # TODO 如果是修改  需要自定关键字参数instance  指定你要修改的实例对象是哪一个
        serializer = BookModelSerializerV2(data=request_data, instance=book_obj)
        serializer.is_valid(raise_exception=True)

        # 经过序列化器对   全局钩子与局部钩子校验后  开始更新
        serializer.save()

        return Response({
            "status": 200,
            "message": '修改成功',
            "results": BookModelSerializerV2(book_obj).data
        })

    # def patch(self, request, *args, **kwargs):
    #     """
    #     整体修改单个:  修改一个对象的全部字段
    #     修改对象时,在调用序列化器验证数据时必须指定instance关键字
    #     在调用serializer.save() 底层是通过ModelSerializer内部的update()方法来完成的更新
    #     """
    #
    #     # 获取要修改的对象的值
    #     request_data = request.data
    #     # 获取要修改的图书的id
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except Book.DoesNotExist:
    #         return Response({
    #             "status": 400,
    #             "message": '图书不存在'
    #         })
    #
    #     # 更新的时候需要对前端传递的数据进行安全校验
    #     # 更新的时候需要指定关键字参数data
    #     # TODO 如果是修改  需要自定关键字参数instance  指定你要修改的实例对象是哪一个
    #     serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 经过序列化器对   全局钩子与局部钩子校验后  开始更新
    #     serializer.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": '修改成功',
    #         "results": BookModelSerializerV2(book_obj).data
    #     })

    def patch(self, request, *args, **kwargs):
        """
        单个: id  传递的修改的内容    1  {book_name: "python"}
        多个: 多个id  多个request.data
        id: [1,2,3]  request.data [{},{},{}]  如何确定要修改的id与值的对应关系
        要求前端传递过来的参数按照一定的格式
        [{pk:1, book_name: "python"},{pk:2, price:300.1},{pk:3, publish: 3}]
        """
        request_data = request.data
        book_id = kwargs.get("id")

        # 如果id存在且传递的request.data格式是字典  单个修改  转成成群体修改一个
        if book_id and isinstance(request_data, dict):
            book_ids = [book_id]
            request_data = [request_data]
        elif not book_id and isinstance(request_data, list):  # 修改多个
            book_ids = []
            # 将所有要修改的图书的id取出放入 book_ids中
            for dic in request_data:
                pk = dic.pop("id", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "PK不存在",
                    })

        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "参数格式有误",
            })

        # print(request_data)
        # print(book_ids)

        # TODO 需要判断传递过来的id对应的图书是否存在  对book_ids 以及 request_data进行筛选
        # TODO 如果id对应的图书不存在  移除id  id对应的request_data也需要移除
        book_list = []  # 所有要修改的图书对象
        new_data = []  # 图书对象对应要修改的值
        for index, pk in enumerate(book_ids):
            # 禁止在循环中对正在循环的列表长度做修改
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])

            except Book.DoesNotExist:
                # 图书对象不存在  则将id与对应的数据移除
                # index = book_ids.index(pk)
                # request_data.pop(index)
                continue

        book_ser = BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "修改成功",
        })


"""
查询单个  查询多个  新增单个
新增多个 删除单个  删除多个  修改单个整体  修改单个  修改多个整体  局部修改多个
"""


# GenericAPIView继承APIView  两者是完全兼容的
# 重点分析GenericAPIView在APIView基础上完成了哪些事情
class BookGenericAPIView(GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin):
    queryset = Book.objects.filter()
    serializer_class = BookModelSerializerV3

    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            # 查询单个
            return self.retrieve(request, *args, **kwargs)
        # 查询所有
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     # 获取book模型中所有的数据
    #     # book_list = Book.objects.filter(is_delete=False)
    #     book_list = self.get_queryset()
    #
    #     # 获取序列化器
    #     # serializer_data = BookModelSerializerV2(book_list, many=True).data
    #     serializer = self.get_serializer(book_list, many=True).data
    #
    #     return Response({
    #         "status": 200,
    #         "message": '查询所有图书成功',
    #         "results": serializer,
    #     })

    # def get(self, request, *args, **kwargs):
    #
    #     # book_id = kwargs.get("pk")
    #     book_obj = self.get_object()
    #     serializer = self.get_serializer(book_obj, many=False).data
    #
    #     return Response({
    #         "status": 200,
    #         "message": '查询所有图书成功',
    #         "results": serializer,
    #     })


class BookGenericAPIViewV3(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializerV3
    lookup_field = "id"



# 登录注册接口
class UserViewSetView(viewsets.GenericViewSet, mixins.ListModelMixin):

    def user_login(self, request, *args, **kwargs):
        request_data = request.data
        username = request_data["username"]
        password = request_data["password"]
        # print(username)
        # print(password)
        serializer = UserModelSerializer(request_data, many=False)
        user = Users.objects.filter(username = username,password=password)
        # print(user)
        if user:
            return Response({
                "status": 200,
                "message": '登录成功',
                "results": serializer.data,
            })
        else:
            return Response({
                "status": 200,
                "message": '用户不存在或密码错误',
                "results": serializer.data,
            })




    def user_register(self,request, *args, **kwargs):
        request_data = request.data
        serializer = UserModelSerializer(data=request_data, many=False)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        # print("注册成功")

        # if user:
        return Response({
            "status": 200,
            "message": '添加成功',
            "results": UserModelSerializer(user_obj, many=False).data,
        })


    def get_user_count(self, request, *args, **kwargs):
        # 完成获取用户数量的逻辑
        print("查询成功")
        return self.list(request, *args, **kwargs)
