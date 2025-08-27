// This stores the entire app layout, including the sidebar and main panel.
import Sidebar from "./Sidebar";
import { Outlet } from "react-router-dom";
export default function Layout() {
  return (
    <div className="flex">
      <Sidebar />
      <main className="main-content">
        <Outlet />
        {/*  This component will be changed by navigating to pages like /tag */}
      </main>
    </div>
  );
}
