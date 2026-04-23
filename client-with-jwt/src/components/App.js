import React, { useEffect, useState } from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import NavBar from "./NavBar";
import Login from "../pages/Login";
import NotesPage from "../pages/NotesPage";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/me", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    }).then((r) => {
      if (r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  const onLogin = (token, user) => {
    localStorage.setItem("token", token);
    setUser(user);
  };

  const onLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  if (!user) return <Login onLogin={onLogin} />;

  return (
    <>
      <NavBar user={user} onLogout={onLogout} />
      <main>
        <Switch>
          <Route exact path="/">
            <Redirect to="/notes" />
          </Route>
          <Route path="/notes">
            <NotesPage />
          </Route>
        </Switch>
      </main>
    </>
  );
}

export default App;
