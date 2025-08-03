import "./App.css";
import React, { useState } from "react";

import Sidebar from "./components/Sidebar";
import TestArea from "./components/TestArea";

const Home = () => <div className="p-4">This is the Home page</div>;
const Library = () => <div className="p-4">This is the Library</div>;
const App: React.FC = () => {
  const [view, setView] = useState("Home");

  let MainComponent;
  switch (view) {
    case "Library":
      MainComponent = <Library />;
      break;
    case "Testing Area":
      MainComponent = <TestArea />;
      break;
    case "Home":
    default:
      MainComponent = <Home />;
      break;
  }
  return (
    <div className="flex">
      <Sidebar setView={setView} />
      <main className="ml-[220px] flex-grow">{MainComponent}</main>
    </div>
  );
};

export default App;
