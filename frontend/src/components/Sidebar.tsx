import React from "react";
import { UserInfo } from "./UserInfo";

interface SidebarProps {
  setView: (view: string) => void;
}

const sidebarItems = ["Home", "Library", "Testing Area"];

const Sidebar: React.FC<SidebarProps> = ({ setView }) => (
  <aside
    style={{
      position: "fixed",
      top: 0,
      left: 0,
      height: "100vh",
      width: "220px",
      display: "flex",
      flexDirection: "column",
      alignItems: "flex-start",
      paddingTop: "20px",
      backgroundColor: "#303030",
      marginBottom: "10px",
    }}
  >
    <div className="text-white text-xl font-semibold mb-4 pl-6">
      Spotify Toolbox
    </div>
    <UserInfo />
    <nav className="w-full">
      <ul className="list-none p-0 m-0 w-full">
        {sidebarItems.map((label) => (
          <li key={label} className="mb-4 px-2 w-full">
            <button
              onClick={() => setView(label)}
              className="w-full text-left px-4 py-2 rounded border border-transparent text-white bg-transparent transition-colors duration-200 hover:border-blue-500 focus:border-white focus:outline-none"
            >
              {label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  </aside>
);

export default Sidebar;
