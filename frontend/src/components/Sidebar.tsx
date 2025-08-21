import React from "react";
import { UserInfo } from "./UserInfo";
import { Link } from "react-router-dom";

const Sidebar: React.FC = () => (
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
    <img src="../../favicon.png" alt="Logo" className="ml-4 w-8 h-8 mb-4" />
    <UserInfo />
    <nav className="w-full">
      <ul className="list-none p-0 m-0 w-full">
        <li key="Library" className="mb-4 px-2 w-full">
          <Link
            to="/library"
            className="w-full text-left px-4 py-2 rounded border border-transparent text-white bg-transparent transition-colors duration-200 hover:border-blue-500 focus:border-white focus:outline-none"
          >
            Library
          </Link>
        </li>
        <li key="Testing Area" className="mb-4 px-2 w-full">
          <Link
            to="/testing"
            className="w-full text-left px-4 py-2 rounded border border-transparent text-white bg-transparent transition-colors duration-200 hover:border-blue-500 focus:border-white focus:outline-none"
          >
            Testing Area
          </Link>
        </li>
      </ul>
    </nav>
  </aside>
);

export default Sidebar;
