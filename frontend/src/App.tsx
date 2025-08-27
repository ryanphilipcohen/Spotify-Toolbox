import React from "react";
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import TestArea from "./components/TestArea";
import Library from "./components/Library";
import TagCreationForm from "./components/TagCreationForm";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="library" element={<Library />} />
        <Route path="testing" element={<TestArea />} />
        <Route path="/tags/create/" element={<TagCreationForm />} />
      </Route>
    </Routes>
  );
};

export default App;
