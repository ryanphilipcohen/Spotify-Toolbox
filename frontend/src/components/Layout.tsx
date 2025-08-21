// This stores the entire app layout, including the sidebar and main panel.
import Sidebar from "./Sidebar";
import { Outlet } from "react-router-dom";
export default function Layout() {
  return (
    <div className="flex">
      <Sidebar />
      <main className="ml-[220px] flex-grow">
        <Outlet />
      </main>
    </div>
  );
}
