import React from "react";

type ButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  variant?: "primary" | "secondary";
  className?: string;
};

export default function Button({
  children,
  onClick,
  type = "button",
  variant = "primary",
  className = "",
}: ButtonProps) {
  const baseStyles =
    "w-full rounded-md py-2 px-4 font-semibold focus:outline-none transition";

  const variants: Record<string, string> = {
    primary: "bg-slate-600 text-white rounded hover:bg-slate-700",
    secondary:
      "bg-white border border-gray-300 text-gray-700 hover:bg-gray-100",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      className={`${baseStyles} ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
