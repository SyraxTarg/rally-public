"use client";
import { useRef, useState } from "react";
import styles from "./code_input.module.css"

export default function CodeInput({code, setCode}) {
  // const [code, setCode] = useState(Array(6).fill(""));
  console.log(code)
  const inputsRef = useRef([]);

  const handleChange = (e, index) => {
    const value = e.target.value;

    if (!/^[0-9]?$/.test(value)) return;

    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);

    if (value && index < 5) {
      inputsRef.current[index + 1].focus();
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1].focus();
    }
  };

  return (
    <div className="flex justify-between gap-2 mb-6">
      {code.map((digit, index) => (
        <input
          key={index}
          ref={(el) => (inputsRef.current[index] = el)}
          type="text"
          inputMode="numeric"
          maxLength={1}
          value={digit}
          onChange={(e) => handleChange(e, index)}
          onKeyDown={(e) => handleKeyDown(e, index)}
          className={`w-12 h-14 text-center text-3xl border rounded-md border-gray-300 focus:ring-2 focus:ring-indigo-500 ${styles.number_input}`}
        />
      ))}
    </div>
  );
}
