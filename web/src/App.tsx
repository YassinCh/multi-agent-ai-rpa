import React from "react";
import Dashboard from "./components/dashboard";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
const queryClient = new QueryClient();
import { RiRobot2Line } from "react-icons/ri";

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
        <header className="header">
        <div className="logo">
          <span className="logo-icon"><RiRobot2Line /></span>
          <span className="logo-text">Multi-Agent AI Visualizer</span>
        </div>
      </header>

      <Dashboard />
    </QueryClientProvider>
  );
}
