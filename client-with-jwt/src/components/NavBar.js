import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { Button } from "../styles";

function NavBar({ user, onLogout }) {
  function handleLogoutClick() {
    localStorage.removeItem("token");
    onLogout();
  }

  return (
    <Wrapper>
      <Logo>
        <Link to="/notes">Notes App</Link>
      </Logo>
      <Nav>
        <Welcome>Welcome, {user.username}!</Welcome>
        <Button as={Link} to="/notes">
          Notes
        </Button>
        <Button variant="outline" onClick={handleLogoutClick}>
          Logout
        </Button>
      </Nav>
    </Wrapper>
  );
}

const Wrapper = styled.header`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
`;

const Logo = styled.h1`
  font-family: "Permanent Marker", cursive;
  font-size: 3rem;
  color: deeppink;
  margin: 0;
  line-height: 1;

  a {
    color: inherit;
    text-decoration: none;
  }
`;

const Nav = styled.nav`
  display: flex;
  gap: 4px;
  position: absolute;
  right: 8px;
  align-items: center;
`;

const Welcome = styled.span`
  font-weight: bold;
  margin-right: 8px;
`;

export default NavBar;
