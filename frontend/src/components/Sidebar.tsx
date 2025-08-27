import React from "react";
import { UserInfo } from "./UserInfo";
import { Link } from "react-router-dom";

const Sidebar: React.FC = () => (
  <aside className="sidebar">
    <img src="../../favicon.png" alt="Logo" className="ml-4 w-8 h-8 mb-4" />
    <div className="sidebar-item">
      <UserInfo />
    </div>
    <nav className="w-full">
      <ul className="list-none p-0 m-0 w-full">
        <li key="Library" className="sidebar-item">
          <Link to="/library" className="block w-full h-full px-4 py-2">
            Library
          </Link>
        </li>
        <li key="Testing Area" className="sidebar-item">
          <Link to="/testing" className="block w-full h-full px-4 py-2">
            Testing Area
          </Link>
        </li>
      </ul>
    </nav>
  </aside>
);

export default Sidebar;
