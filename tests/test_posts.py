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
  assert res.json()['detail'] == "Not authenticated"
  assert res.status_code == 401

def test_authed_user_get_non_existing_post(authorized_client, test_posts):
  res = authorized_client.get("/posts/888888888")
  assert res.json()['detail'] == 'Post with id: 888888888 was not found.'
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
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
  res = authorized_client.post("/posts/", json = { "title": title,
                                                    "content": content,
                                                    "published": published })
  created_post = PostResponse(**res.json())
  assert res.status_code == 201
  assert created_post.title == title
  assert created_post.content == content
  assert created_post.published == published
  assert created_post.owner_id == test_user["id"]

@pytest.mark.parametrize( "title, content", [
    ("title 1", "content 1 !   !"),
    ("title 2", "content 2 !!  !"),
    ("title 3", "content 3 ! ! !"),
  ])
def test_create_post_default_published(authorized_client, test_user, test_posts, title, content):
  res = authorized_client.post("/posts/", json = { "title": title,
                                                    "content": content })
  created_post = PostResponse(**res.json())
  assert res.status_code == 201
  assert created_post.title == title
  assert created_post.content == content
  assert created_post.published == True
  assert created_post.owner_id == test_user["id"]

def test_unauthed_user_create_posts(client, test_posts):
  res = client.post("/posts/", json = { "title": "title1",
                                        "content": "content1" })
  assert res.json()['detail'] == "Not authenticated"
  assert res.status_code == 401

def test_unauthed_user_delete_posts(client, test_posts):
  res = client.delete(f"/posts/{test_posts[0].id}")
  assert res.json()['detail'] == "Not authenticated"
  assert res.status_code == 401

def test_authed_user_delete_posts(authorized_client, test_posts):
  res = authorized_client.delete(f"/posts/{test_posts[0].id}")
  assert res.status_code == 204

def test_authed_user_delete_non_existing_post(authorized_client, test_posts):
  res = authorized_client.delete("/posts/888888888")
  assert res.json()['detail'] == 'Post with id: 888888888 was not found.'
  assert res.status_code == 404

def test_authed_user_delete_other_users_post(authorized_client, test_posts):
  res = authorized_client.delete(f"/posts/{test_posts[3].id}")
  assert res.json()['detail'] == "Not authorized to perform requested action"
  assert res.status_code  == 403

@pytest.mark.parametrize( "title, content, published", [
    ("title update1", "content update1 !   !", True),
    ("title update2", "content update2 !!  !", False)
  ])
def test_update_post(authorized_client, test_user, test_posts, title, content, published):
  res = authorized_client.put(f"/posts/{test_posts[0].id}", json = { "title": title,
                                                   "content": content,
                                                   "published": published})
  update_post = PostResponse(**res.json())
  assert res.status_code == 200
  assert update_post.title == title
  assert update_post.content == content
  assert update_post.published == published
  assert update_post.owner_id == test_user["id"]

@pytest.mark.parametrize( "title, content, published", [
    ("title update1", "content update1 !   !", True),
    ("title update2", "content update2 !!  !", False)
  ])
def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts, title, content, published):
  res = authorized_client.put(f"/posts/{test_posts[3].id}", json = { "title": title,
                                                   "content": content,
                                                   "published": published,})
  assert res.status_code == 403
  assert res.json()['detail'] == 'Not authorized to perform requested action'

@pytest.mark.parametrize( "title, content, published", [
    ("title update1", "content update1 !   !", True),
    ("title update2", "content update2 !!  !", False)
  ])
def test_unauthorized_user_update_post(client, test_user, test_user2, test_posts, title, content, published):
  res = client.put(f"/posts/{test_posts[3].id}", json = { "title": title,
                                                          "content": content,
                                                          "published": published,})
  assert res.status_code == 401
  assert res.json()['detail'] == 'Not authenticated'

@pytest.mark.parametrize( "title, content, published", [
    ("title update1", "content update1 !   !", True),
    ("title update2", "content update2 !!  !", False)
  ])
def test_authed_user_update_non_existing_post(authorized_client, test_posts, title, content, published):
  res = authorized_client.put("/posts/888888888", json = { "title": title,
                                                           "content": content,
                                                           "published": published,})
  assert res.json()['detail'] == 'Post with id: 888888888 was not found.'
  assert res.status_code == 404
