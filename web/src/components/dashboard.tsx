import React from "react";
import Graph from "./graph";
import { ReactFlowProvider } from "@xyflow/react";

export default function Dashboard() {
  return (
    <ReactFlowProvider>
      <Graph />
    </ReactFlowProvider>
  );
}
