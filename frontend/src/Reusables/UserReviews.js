import Picture from "../Misc/user-pic.jpg";

function UserReviews() {
  const users = [
    {
      name: "Sarah L. - Codeforces Enthusiast",
      content:
        "AICAP changed how I approach Codeforces challenges. The insights into my progress and the problem recommendations have been incredibly helpful. It’s like having a personal coding mentor!",
    },
    {
      name: "Alex M. - Aspiring Algorithmist",
      content:
        "The intelligence behind AICAP is mind-blowing. The problem suggestions are tailored to my strengths and weaknesses. It’s like having a personal coach. My confidence in contests has soared, all thanks to this incredible platform",
    },
    {
      name: "Raj T. - Competitive Programmer",
      content:
        "As a competitive programmer, precision matters. AICAP's rating predictor proved spot-on! It kept me motivated, knowing exactly when I'd hit my goal. The community here is fantastic too, full of helpful, like-minded individuals.",
    },
  ];

  return (
    <div class="user-reviews">
      {users.map((user) => {
        return (
          <div className="review">
            <div>
              <h4>{user.name}</h4>
              <p>{user.content}</p>
            </div>
            <img src={Picture} alt="Profile"></img>
          </div>
        );
      })}
    </div>
  );
}

export default UserReviews;
