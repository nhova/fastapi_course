from app.schemas.post import PostOut, PostCreate, PostResponse
import pytest

def test_authed_user_get_all_posts(authorized_client, test_posts):
  res = authorized_client.get("/posts/")
  def validate(post):
    return PostOut(**post)
  posts_map = map(validate, res.json())
  assert len(res.json()) == len(test_posts)
  assert res.status_code == 200

def test_unauthed_user_get_all_posts(client, test_posts):
  res = client.get("/posts/")
  assert res.status_code == 401

def test_unauthed_user_get_one_posts(client, test_posts):
  res = client.get(f"/posts/{test_posts[0].id}")
  assert res.status_code == 401

def test_authed_user_get_non_existing_post(authorized_client, test_posts):
  res = authorized_client.get("/posts/888888888")
  assert res.status_code == 404

def test_authed_user_get_one_posts(authorized_client, test_posts):
  res = authorized_client.get(f"/posts/{test_posts[0].id}")
  post = PostOut(**res.json())
  assert post.PostModel.id == test_posts[0].id
  assert post.PostModel.content == test_posts[0].content
  assert post.PostModel.title == test_posts[0].title
  assert res.status_code == 200

@pytest.mark.parametrize( "title, content, published", [
    ("title 1", "content 1 !   !", True),
    ("title 2", "content 2 !!  !", False),
    ("title 3", "content 3 ! ! !", True),
    ('title 4', 'content 4 !  !!', False),
  ])
def test_create_post(authorized_client, test_user,  title, content, published):
  res = authorized_client.post("/posts/", json = { "title": title,
                                                    "content": content,
                                                    "published": published })
  created_post = PostResponse(**res.json())
  assert res.status_code == 201
  assert created_post.title == title
  assert created_post.content == content
  assert created_post.published == published
  assert created_post.owner_id == test_user["id"]
