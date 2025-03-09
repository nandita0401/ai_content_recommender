"use client"; // Required for client-side rendering

import { useEffect, useState } from "react";
import axios from "axios";

interface Movie {
  id: number;
  title: string;
  genre: string;
  rating: number;
  poster: string;
  imdb_url: string;
  reason?: string;
  imdb_id: number;
}

interface TrendingMovie {
  title: string;
  poster: string;
  rating: string;
  imdb_url: string;
}

export default function Home() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [recommendations, setRecommendations] = useState<Movie[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [trending, setTrending] = useState<TrendingMovie[]>([]);

  useEffect(() => {
    // Fetch All Movies
    axios
      .get("http://127.0.0.1:8000/movies")
      .then((res) => setMovies(res.data))
      .catch(() => setError("Failed to fetch movies."));

    // Fetch Personalized Recommendations
    axios
      .get("http://127.0.0.1:8000/recommendations/1")
      .then((res) => setRecommendations(res.data))
      .catch(() => setError("Failed to fetch recommendations."));

    // Fetch Trending Movies
    axios
      .get("http://127.0.0.1:8000/trending")
      .then((res) => setTrending(res.data))
      .catch(() => console.error("Failed to fetch trending movies."));
  }, []);

  return (
    <main className="p-6 min-h-screen bg-gradient-to-b from-gray-900 via-black to-gray-900 text-white">
      <h1 className="text-4xl font-extrabold mb-6 border-b-2 border-yellow-400 pb-2">🎬 Recommended Movies</h1>

      {error && <p className="text-red-500">{error}</p>}

      {/* Trending Movies Section */}
      <h2 className="text-2xl font-semibold mt-6 text-center">🔥 Trending Movies</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 justify-center">
        {movies.map((movie) => (
          <div key={movie.imdb_id} className="bg-gray-900 p-4 rounded-lg shadow-lg text-center">
            <a href={movie.imdb_url} target="_blank" rel="noopener noreferrer">
              <div className="hover:scale-105 transition-transform duration-300 ease-in-out">
                <img 
                  src={movie.poster || "https://via.placeholder.com/140x207"} 
                  alt={movie.title} 
                  className="transition-opacity duration-700 opacity-0 w-full h-64 object-cover rounded-lg shadow-lg" 
                  onLoad={(e) => e.currentTarget.classList.add('opacity-100')}
                />
              </div>
            </a>
            <h3 className="text-xl font-bold mt-3 text-center">{movie.title} ({movie.genre})</h3>
            <p className="text-yellow-400 text-lg text-center">⭐ {movie.rating}</p>
          </div>
        ))}
      </div>

      {/* Trending Now Section */}
      <h2 className="text-2xl font-semibold mt-6 text-center">🔥 Trending Now</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 justify-center">
        {trending.map((movie) => (
          <div key={movie.imdb_url} className="bg-gray-900 text-white rounded-lg shadow-lg overflow-hidden">
            <a href={movie.imdb_url} target="_blank" rel="noopener noreferrer">
              <div className="hover:scale-105 transition-transform duration-300 ease-in-out">
                <img 
                  src={movie.poster || "https://via.placeholder.com/140x207"} 
                  alt={movie.title} 
                  className="transition-opacity duration-700 opacity-0 w-full h-64 object-cover rounded-lg shadow-lg" 
                  onLoad={(e) => e.currentTarget.classList.add('opacity-100')}
                />
              </div>
            </a>
            <div className="p-4">
              <h3 className="text-lg font-semibold">{movie.title}</h3>
              <p className="text-yellow-400">⭐ {movie.rating}</p>
          </div>
        </div>
        ))}
      </div>

      {/* Personalized Recommendations */}
      <h2 className="text-2xl font-semibold mt-6 text-center">✨ Personalized for You</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 justify-center">
        {recommendations.map((movie) => (
          <div key={movie.imdb_id} className="bg-gray-800 text-white rounded-lg shadow-lg overflow-hidden">
            <a href={movie.imdb_url} target="_blank" rel="noopener noreferrer">
              <div className="hover:scale-105 transition-transform duration-300 ease-in-out">
                <img 
                  src={movie.poster || "https://via.placeholder.com/140x207"} 
                  alt={movie.title} 
                  className="transition-opacity duration-700 opacity-0 w-full h-64 object-cover rounded-lg shadow-lg" 
                  onLoad={(e) => e.currentTarget.classList.add('opacity-100')}
                />
              </div>
            </a>
            <div className="p-4">
              <h3 className="text-lg font-semibold text-center">{movie.title} ({movie.genre})</h3>
              <p className="text-yellow-400 text-center">⭐ {movie.rating}</p>
              {movie.reason && <p className="text-sm text-gray-400 mt-2 text-center">🎯 {movie.reason}</p>}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
