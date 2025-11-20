import { Link } from "react-router"; // use react-router-dom for web apps
import { FaExclamationTriangle } from "react-icons/fa"; // Font Awesome icon

export function Error() {
  return (
    <div className="flex flex-col items-center justify-center px-4 text-center">
      <div className="flex flex-col items-center space-y-4">
        <FaExclamationTriangle className="text-red-500 text-6xl" />
        <h1 className="text-2xl font-semibold text-gray-800">Oops! Something went wrong.</h1>
        <p className="text-gray-600">
          We couldn’t process your request. Please try again later or return to the homepage.
        </p>
        <Link to="/" className="inline-block">
          <button className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-full transition">
            Go to Home
          </button>
        </Link>
      </div>
    </div>
  );
}