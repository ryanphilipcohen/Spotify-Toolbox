import React from "react";
import TrackLibrary from "./TrackLibrary";
import TagLibrary from "./TagLibrary";

const Catalogs = () => <div className="text-white">Catalogs view content</div>;

const Library: React.FC = () => {
  let ViewComponent;
  let [libraryView, setLibraryView] = React.useState("Tracks");

  switch (libraryView) {
    case "Tags":
      ViewComponent = <TagLibrary />;
      break;
    case "Catalogs":
      ViewComponent = <Catalogs />;
      break;
    case "Tracks":
    default:
      ViewComponent = <TrackLibrary />;
      break;
  }

  return (
    <div className="p-4">
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setLibraryView("Tracks")}
          className="text-left px-4 py-2 rounded border border-transparent text-white bg-transparent transition-colors duration-200 hover:border-blue-500 focus:border-white focus:outline-none"
        >
          Tracks
        </button>
        <button
          onClick={() => setLibraryView("Tags")}
          className="text-left px-4 py-2 rounded border border-transparent text-white bg-transparent transition-colors duration-200 hover:border-blue-500 focus:border-white focus:outline-none"
        >
          Tags
        </button>
        <button
          onClick={() => setLibraryView("Catalogs")}
          className="text-left px-4 py-2 rounded border border-transparent text-white bg-transparent transition-colors duration-200 hover:border-blue-500 focus:border-white focus:outline-none"
        >
          Catalogs
        </button>
      </div>
      {ViewComponent}
    </div>
  );
};

export default Library;
