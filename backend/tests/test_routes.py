import responses

from backend.app.extensions import db
from backend.app.models.models import User


def test_home(client):
    response = client.get("/")
    assert b'<p>Hello, World!</p>' in response.data


@responses.activate
def test_add_user_route_working(app, client):
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.status?handle=Mex7",
        json=get_mock_submissions()
    )
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.info?handles=Mex7",
        json=get_mock_user()
    )

    response = client.post("/users/Mex7")

    with app.app_context():
        user_obj = db.session.execute(db.select(User)).scalar()

    assert response.status_code == 200
    assert user_obj is not None
    assert user_obj.handle == "Mex7"
    assert user_obj.rating == 1450
    assert user_obj.rank == "specialist"
    assert user_obj.max_rating == 1600


@responses.activate
def test_add_user_route_invalid_handle(client):
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.info?handles=invalid_name",
        json={
            "status": "FAILED",
            "message": "User not found"
        },
        status=200
    )

    response = client.post("/users/invalid_name")

    assert response.status_code == 404
    assert b"User not found" in response.data


@responses.activate
def test_add_user_route_codeforces_not_working(client):
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.info?handles=codeforces_is_broken",
        json={"message": "Codeforces not available at the moment"},
        status=500
    )

    response = client.post("/users/codeforces_is_broken")
    assert response.status_code == 500
    assert b"Codeforces not available" in response.data


@responses.activate
def test_user_solved_problems_route_working(client):
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.status?handle=Mex7",
        json=get_mock_submissions()
    )
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.info?handles=Mex7",
        json=get_mock_user()
    )

    response = client.post("/users/Mex7")
    response = client.get("/problems/Mex7")

    assert response.status_code == 200
    assert response.json["problems_solved"][0]["id"] == "1800A"


def test_user_solved_problems_not_working(client):
    response = client.get("/problems/Not_Existing_User")

    assert response.status_code == 404
    assert response.json["status"] == "FAILED"


def test_predict_rating_not_provided(client):
    response = client.get("/predict/Mex7")

    assert response.status_code == 401
    assert response.json["status"] == "FAILED"
    assert response.json["message"] == "You should provide a desired rating"


@responses.activate
def test_recommend_not_working(client):
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.info?handles=Mex",
        json={"status": "FAILED", "message": "Codeforces not available at the moment"},
        status=500
    )

    response = client.get("/recommend/Mex")

    assert response.status_code == 500
    assert response.json["status"] == "FAILED"
    assert response.json["message"] == "An error has occurred, try again later"


@responses.activate
def test_recommend_working(client):
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.status?handle=User",
        json=get_mock_submissions(),
        status=200
    )
    responses.add(
        responses.GET,
        "https://codeforces.com/api/user.info?handles=User",
        json=get_mock_user(),
        status=200
    )
    response = client.get("/recommend/User")

    assert response.status_code == 200


def get_mock_submissions():
    return {
        "status": "SUCCESS",
        "result": [{
            "verdict": "OK",
            "contestId": 1800,
            "problem": {
                "contestId": 1800,
                "index": "A",
                "rating": 1500,
                "tags": ["dp", "combinatorics"],
                "name": "Problem 1"
            }
        }, {
            "verdict": "FAILED",
            "contestId": 1456,
            "problem": {
                "contestId": 1456,
                "index": "C",
                "rating": 1600,
                "tags": ["math", "greedy"],
                "name": "Problem 2"
            }
        }]
    }


def get_mock_user():
    return {
        "status": "SUCCESS",
        "result": [{
            "handle": "Mex7",
            "rating": 1450,
            "maxRating": 1600,
            "avatar": "www.avatar.mex/mex12345profile",
            "rank": "specialist"
        }]
    }
