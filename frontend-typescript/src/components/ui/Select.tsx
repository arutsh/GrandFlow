import React from "react";

type Option = {
  label: string;
  value: string;
};

type SelectProps = {
  label?: string;
  name: string;
  value?: string;
  options: Option[];
  onChange?: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  required?: boolean;
  showLabel?: boolean;
  disabled?: boolean;
  placeholder?: string;
  allowCreate?: boolean;
  createLabel?: string;
};

export default function Select({
  label = "",
  name,
  value,
  options,
  onChange,
  required = false,
  showLabel = true,
  disabled = false,
  placeholder = "-- Select --",
  allowCreate = false,
  createLabel = "➕ Create new...",
}: SelectProps) {
  const combinedOptions = allowCreate
    ? [...options, { label: createLabel, value: "__new" }]
    : options;

  return (
    <div className="mb-4">
      {showLabel && (
        <label
          htmlFor={name}
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}

      <select
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white focus:outline-none focus:ring-brand-blue focus:border-brand-blue sm:text-sm"
      >
        <option value="">{placeholder}</option>
        {combinedOptions.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}
