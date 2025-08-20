from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from src.adapters.posts import (
    create_in_to_internal,
    create_internal_to_out,
    post_internal_to_out,
)
from src.assembly import build_post_controller
from src.controllers.post_controller import PostController
from src.database.config import get_db
from src.models.incoming.create_post_request import CreatePostRequest
from src.models.internal.post_filter import PostFilter
from src.models.out.create_post_response import CreatePostResponse
from src.models.out.delete_post import DeletePostResponse
from src.models.out.get_posts_count import GetPostsCountResponse
from src.models.out.post_response import PostResponse
from src.models.out.reset import ResetResponse

router = APIRouter(prefix="/posts")


@router.post(
    "/", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(
    post: CreatePostRequest,
    controller: PostController = Depends(build_post_controller),
    db=Depends(get_db),
) -> CreatePostResponse:
    new_post = controller.create_post(db, create_in_to_internal(post))
    return create_internal_to_out(new_post)


@router.get(
    "/count", response_model=GetPostsCountResponse, status_code=status.HTTP_200_OK
)
def get_posts_count(
    controller: PostController = Depends(build_post_controller),
    db=Depends(get_db),
) -> GetPostsCountResponse:
    count = controller.get_count(db)
    return GetPostsCountResponse(count=count)


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"


@router.post("/reset", response_model=ResetResponse, status_code=status.HTTP_200_OK)
def reset(
    controller: PostController = Depends(build_post_controller),
    db=Depends(get_db),
) -> ResetResponse:
    controller.reset(db)
    return ResetResponse(msg="Todos los datos fueron eliminados")


@router.get("/", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
def get_posts(
    expire: bool | None = Query(
        None,
        description="Returns expired posts if true, otherwise returns active posts",
    ),
    route: UUID = Query(None, description="Filter posts by route ID"),
    owner: UUID = Query(None, description="Filter posts by user ID"),
    controller: PostController = Depends(build_post_controller),
    db=Depends(get_db),
) -> list[PostResponse]:
    posts = controller.get_posts(
        db, PostFilter(expire=expire, route=route, owner=owner)
    )
    return [post_internal_to_out(post) for post in posts]


@router.get("/{id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(
    id: UUID = Path(description="The ID of the post to retrieve"),
    controller: PostController = Depends(build_post_controller),
    db=Depends(get_db),
) -> PostResponse:
    post = controller.get_post(db, id)
    return post_internal_to_out(post)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(
    id: UUID = Path(description="The ID of the post to retrieve"),
    controller: PostController = Depends(build_post_controller),
    db=Depends(get_db),
) -> DeletePostResponse:
    controller.delete_post(db, id)
    return DeletePostResponse(msg="la publicación fue eliminada")
