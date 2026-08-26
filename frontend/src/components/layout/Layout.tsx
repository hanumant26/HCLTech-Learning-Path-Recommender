import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import AIAssistant from "../assistant/AIAssistant";

export default function Layout() {
  return (
    <div className="min-h-screen bg-paper">
      <Navbar />
      <main>
        <Outlet />
      </main>
      <AIAssistant />
    </div>
  );
}
