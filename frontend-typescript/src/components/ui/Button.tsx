import React, { useState } from "react";

type ButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  variant?: "primary" | "secondary" | "danger";
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
    danger: "bg-red-600 text-white rounded hover:bg-red-700",
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

interface ConfirmDeleteButtonProps {
  onConfirm: () => void;
  className?: string;
}
export function ConfirmDeleteButton({
  onConfirm,
  className = "",
  children,
}: ConfirmDeleteButtonProps) {
  const [confirming, setConfirming] = useState(false);

  if (confirming) {
    return (
      <div className="flex space-x-2">
        <Button
          variant="danger"
          onClick={() => {
            onConfirm();
            setConfirming(false);
          }}
          className={className}
        >
          Yes
        </Button>
        <Button
          variant="secondary"
          onClick={() => setConfirming(false)}
          className={className}
        >
          No
        </Button>
      </div>
    );
  }

  return (
    <Button
      variant="danger"
      onClick={() => setConfirming(true)}
      className={className}
    >
      {children || "Delete"}
    </Button>
  );
}
