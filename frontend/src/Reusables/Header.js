import image from "../Misc/logo-cover.png";

function Header() {
  return (
    <div className="header-background">
      <img src={image} alt="logo" className="logo"></img>
    </div>
  );
}

export default Header;
