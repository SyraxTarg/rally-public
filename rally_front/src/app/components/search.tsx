"use client";
import { useState } from "react";
import styles from "./search.module.css"

type SearchBarProps = {
  onSearch: (searchTerm: string) => void;
  prop_type: string;
};

const SearchBar = ({ onSearch, prop_type }: SearchBarProps) => {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(searchTerm.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center space-x-2 w-full max-w-md mx-auto my-6">
      <input
        type="text"
        placeholder={`Rechercher un ${prop_type}...`}
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full px-4 py-2 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        className={`px-4 py-2 ${styles.search_button} text-white rounded-xl transition duration-200`}
      >
        Rechercher
      </button>
    </form>
  );
};

export default SearchBar;
