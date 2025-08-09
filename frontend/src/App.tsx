import "./App.css";
import React, { useState } from "react";

import Sidebar from "./components/Sidebar";
import TestArea from "./components/TestArea";
import Library from "./components/Library";

const App: React.FC = () => {
  const [sidebarView, setSidebarView] = useState("Library");
  const [libraryView, setLibraryView] = useState("Tracks");

  let MainComponent;
  switch (sidebarView) {
    case "Testing Area":
      MainComponent = <TestArea />;
      break;
    case "Library":
    default:
      MainComponent = (
        <Library libraryView={libraryView} setLibraryView={setLibraryView} />
      );
      break;
  }
  return (
    <div className="flex">
      <Sidebar setSidebarView={setSidebarView} />
      <main className="ml-[220px] flex-grow">{MainComponent}</main>
    </div>
  );
};

export default App;
