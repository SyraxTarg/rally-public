"use client";
import { useState, useEffect } from "react";

type CustomDatePickerProps = {
  label?: string;
  value?: string | null; // format YYYY-MM-DD or null
  onChange: (date: string | null) => void;
};

export default function CustomDatePicker({
  label = "Choisir une date",
  value,
  onChange,
}: CustomDatePickerProps) {
  const [internalValue, setInternalValue] = useState(value || "");

  // 🆕 Sync avec les props quand value change depuis le parent
  useEffect(() => {
    setInternalValue(value || "");
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const date = e.target.value;
    console.log(date);
    setInternalValue(date);

    if (date === "") {
      onChange(null); // réinitialise
    } else if (/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      onChange(date);
    }
  };

  return (
    <div className="flex flex-col gap-1 mb-4">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <input
        type="date"
        value={internalValue}
        onChange={handleChange}
        className="border border-gray-300 rounded px-3 py-2 text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-400"
      />
      {!internalValue && (
        <span className="text-xs text-gray-400 italic">jj/mm/yyyy</span>
      )}
    </div>
  );
}
