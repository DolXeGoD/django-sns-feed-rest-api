from django.http import Http404, HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FeedListSerializer, FeedDetailSerializer, FeedCreateSerializer, CommentCreateSerializer, \
    CommentListSerializer, CommentUpdateSerializer, CommentDeleteSerializer

from .models import Feed,Comment,Like

# Create your views here.

class FeedList(APIView):
    def post(self, request): # 피드 작성
        serializer_class = FeedCreateSerializer(data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors)

    def get(self, request): # 피드 전체 리스트
        queryset = Feed.objects.all().order_by('-feed_id') # 피드 내림차순 정렬
        serializer_class = FeedListSerializer(queryset, many=True)
        return Response(serializer_class.data)

class FeedDetail(APIView):
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer

    def get_feed(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk): # 피드 상세 조회
        feed = self.get_feed(pk)
        serializer_class = FeedDetailSerializer(feed)

        # response에 좋아요, 댓글, 공유 카운트 추가
        additional_data = {"like_count": str(feed.get_like_count()),
                           "comment_count": str(feed.get_comment_count()),
                           "share_count": str(feed.get_share_count())}
        additional_data.update(serializer_class.data)

        return Response(additional_data)

class CommentList(APIView):
    def post(self, request, pk): # 댓글 작성
        serializer_class = CommentCreateSerializer(data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors)

    def get(self, request, pk): # 댓글 리스트 조회
        feed = get_object_or_404(Feed, pk=pk)
        queryset = feed.comment_set
        serializer_class = CommentListSerializer(queryset, many=True)
        return Response(serializer_class.data)

class CommentDetail(APIView):
    def get(self, request, pk, cpk): # 댓글 상세 조회 (테스트용)
        feed = get_object_or_404(Feed, pk=pk)
        queryset = feed.comment_set.get(pk=cpk)
        serializer_class = CommentListSerializer(queryset)
        return Response(serializer_class.data)

    def put(self, request, pk, cpk): # 댓글 수정
        feed = get_object_or_404(Feed, pk=pk)
        comment = feed.comment_set.get(pk=cpk)
        serializer_class = CommentUpdateSerializer(comment, data=request.data)

        if serializer_class.is_valid():
            if request.data["user_id"] == comment.user_id:
                serializer_class.save()
                return Response(serializer_class.data)
            else:
                return Response('본인이 작성한 글만 수정할 수 있습니다.', status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('요청 파라미터가 부족합니다.', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, cpk): # 댓글 삭제
        feed = get_object_or_404(Feed, pk=pk)
        comment = feed.comment_set.get(pk=cpk)
        serializer_class = CommentDeleteSerializer(data=request.data)

        if serializer_class.is_valid():
            if request.data["user_id"] == comment.user_id:
                comment.delete()
                return Response('댓글을 삭제하였습니다.', status=status.HTTP_204_NO_CONTENT)
            else:
                return Response('본인이 작성한 글만 삭제할 수 있습니다.', status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('요청 파라미터가 부족합니다.', status=status.HTTP_400_BAD_REQUEST)

class LikeDetail(APIView):
    def post(self, request, pk): # 좋아요 추가
        feed = get_object_or_404(Feed, pk=pk)
        try:
            like = Like(feed_id=feed, user_id=request.data["user"])
            like.save()
            return Response('좋아요가 추가되었습니다.')
        except Exception as e:
            like = Like.objects.get(feed_id=feed, user_id=request.data["user"])
            like.delete()
            return Response('좋아요를 삭제하였습니다.')

