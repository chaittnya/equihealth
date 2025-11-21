import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import MainLayout from "./components/layout/MainLayout.jsx";

import routes from "./routes/Routes.jsx";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          {routes.map(({ path, element }, index) => (
            <Route key={index} path={path} element={element} />
          ))}
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
