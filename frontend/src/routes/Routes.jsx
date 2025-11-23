import Home from "../pages/Home";
import FileComplaint from "../pages/FileComplaint";
import AnalyticsDashboard from "../pages/AnalyticsDashboard";
import ComplaintHistory from "../pages/ComplaintHistory";

const routes = [
  { path: "/", element: <Home /> },
  { path: "/file-complaint", element: <FileComplaint /> },
  { path: "/analytics", element: <AnalyticsDashboard /> },
  { path: "/complaints", element: <ComplaintHistory /> },
];

export default routes;
